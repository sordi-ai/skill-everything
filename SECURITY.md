# Security policy
*The threat model is the product. This file is the contract.*

> **skill-everything applies standard supply-chain rigor to agent rule learning.** The same toolkit an npm-package gets — schema validation, lint, CODEOWNERS, branch protection — applies to every `learn(errors):` rule the agent proposes. *That's the architecture. This document spells it out.*

---

## REPORTING A VULNERABILITY
*Email private, do not file a public issue.*

> [!CAUTION]
> **Do not file a public issue.** A public report can be exploited before a fix lands.

Email `security@sordi.ai` (PGP key on request) with:

1. A description of the issue and the affected files / lines.
2. A reproducer if possible.
3. Whether you have already disclosed the issue elsewhere.

Expected first reply: within 7 days. We are an independent two-person side project — we do not have an SLA, but we take reports seriously. `blank_issues_enabled` is set to `false` in `.github/ISSUE_TEMPLATE/config.yml` to keep accidental security disclosures from landing in public issues.

---

## THREAT MODEL
*Self-extending memory means rules are executable input. This is the threat.*

Skill-Everything is a self-extending memory system: an agent writes rules into `skills/error-log/*.md` and those rules are read by every subsequent agent session as instructions. **The rules are executable input.**

![PR flow — agent branch through lint-rules and auto-approve-rule-pr CI gates, CODEOWNERS human gate, squash-merge into main behind branch protection](./docs/pr-flow.svg)

*Branch through CI gates and CODEOWNERS into a squash-merge on `main`.*

### Asset

The contents of `skills/**`. Every rule is consumed as instruction by downstream consumers of this repository.

### Trust boundaries

- `main` branch is trusted. Anyone who can land a commit on `main` can re-program every consumer.
- PR contributions are untrusted until reviewed.
- Self-extension commits authored by an agent are untrusted until a human reviews the PR.

### Adversaries

| Adversary | Goal | Mitigations |
|---|---|---|
| External PR contributor | Insert a rule that exfiltrates credentials, runs shell, or nudges next-session agent toward bad actions | `lint-rules` CI · `.github/CODEOWNERS` requires maintainer approval on `skills/error-log/` · branch protection (see required GitHub setting below) · human PR review |
| Prompt-injection via task input | Trick the running agent into writing a poisoned `new_rule` that gets committed | Same as above; the lint-rules CI is best-effort, not airtight (see Limitations below) |
| Honest contributor pasting prod data | Leak PII / secrets into `error-log.md` | `gitleaks` pre-commit · explicit redaction reminder in `.github/ISSUE_TEMPLATE/error-capture.md` |

*Three adversary classes, three mitigation layers. None are individually sufficient — defence-in-depth.*

### Limitations — what the validator catches and what it doesn't

> **Defense-in-depth via deterministic validation:** verb allow-list, schema validation, forbidden-pattern set, plus required CODEOWNERS approval. The adversarial test suite documents the validator boundary explicitly.

The CI rule validator (`tools/validate_rules.py`) implements deterministic checks:

- It allow-lists starting verbs and rejects an explicit set of forbidden patterns (URLs, shell binaries, credential paths, `<script>` tags, base64-shaped strings).
- It complements rather than replaces semantic review — the [`tests/test_validate_rules_adversarial.py`](./tests/test_validate_rules_adversarial.py) suite documents the boundary between structural and semantic threats (homoglyphs, indirection, natural-language nudges).
- It is a static check, paired with required CODEOWNERS review for semantic coverage.

> [!NOTE]
> **CI-validated. CODEOWNERS-required when branch protection is enabled.** Every rule passes the deterministic validator before merge. [`.github/CODEOWNERS`](./.github/CODEOWNERS) declares maintainer approval on `skills/error-log/`, but this declaration only blocks merges if the repository's branch protection is configured to "Require review from Code Owners" — that is a GitHub setting, not a committed file. See [Required GitHub branch-protection on `main`](#required-github-branch-protection-on-main) below for the exact list. The adversarial test suite is part of the public engineering record and runs on every PR.

---

## REQUIRED GITHUB BRANCH-PROTECTION ON `main`
*Eight settings. All required for the threat model to hold.*

> [!WARNING]
> **HUMAN GATE · branch protection** — Branch protection is required, not optional. Without it the trust boundary collapses — anyone with write access can land an unreviewed `learn(errors)` commit.

To make the threat model effective, the repository owner must enable (Settings → Branches → Branch protection rules → `main`):

| Setting | Value | Why |
|---|---|---|
| `Require a pull request before merging` | at least 1 approving review | Forces every change through review |
| `Require status checks to pass` | `lint-rules`, `ci / test (3.12, ubuntu)` | Validator + test suite must pass |
| `Require branches up to date` | enabled | No stale-branch merges |
| `Require linear history` | squash-merge default | Clean blame, reverts work |
| `Restrict who can push` | including admins | Prevents accidental admin override |
| `Allow force pushes` | disabled | History is forensic evidence |
| `Allow deletions` | disabled | No silent branch removal |
| `Require review from Code Owners` | enabled (uses `.github/CODEOWNERS`) | Maintainer must see rule changes |

*`Require signed commits` is **Phase 2** — it raises the barrier for external contributors and is deferred until the project has co-maintainers.*

---

## RECOVERY RUNBOOK FOR SECRET LEAKAGE
*If an API key, JWT, customer ID, or internal hostname lands in the tree.*

> [!CAUTION]
> **`git revert` is not enough.** A revert keeps the secret in git history. Rotation is the only fully effective mitigation.

1. Rotate the leaked secret at its source immediately.
2. Use `git filter-repo` to rewrite history:
   ```bash
   pip install git-filter-repo
   git filter-repo --invert-paths --path <file>
   # or replace the secret in place:
   git filter-repo --replace-text replacements.txt
   ```
3. Force-push the rewritten branch and notify all forks / clones to re-clone (`git pull` will fail and show the divergence):
   ```bash
   git push --force-with-lease origin main
   ```
4. Open a [GitHub Security Advisory](https://github.com/sordi-ai/skill-everything/security/advisories/new) so downstream users get notified.

`git filter-repo` is not bundled with git — install via `pip install git-filter-repo`.
