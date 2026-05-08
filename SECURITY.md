# Security Policy

## Reporting a vulnerability

**Please do not file a public issue.** Instead, email `security@sordi.ai` (PGP key on request) with:

1. A description of the issue and the affected files / lines.
2. A reproducer if possible.
3. Whether you have already disclosed the issue elsewhere.

Expected first reply: within 7 days. We are an independent two-person side project — we do not have an SLA, but we take reports seriously.

`blank_issues_enabled` is set to `false` in `.github/ISSUE_TEMPLATE/config.yml` to keep accidental security disclosures from landing in public issues.

---

## Threat model

Skill-Everything is a **self-extending memory system**: an agent writes rules into `references/errors/*.md` and those rules are read by every subsequent agent session as instructions. **The rules are executable input.** This is the threat model:

### Asset

- The contents of `references/**`. Every rule is consumed as instruction by downstream consumers of this repository.

### Trust boundaries

- `main` branch is trusted. Anyone who can land a commit on `main` can re-program every consumer.
- PR contributions are untrusted until reviewed.
- Self-extension commits authored by an agent are untrusted until a human reviews the PR.

### Adversaries

| | Goal | Mitigations |
|---|---|---|
| External PR contributor | Insert a rule that exfiltrates credentials, runs shell, or nudges next-session agent toward bad actions | CI lint-rules · CODEOWNERS approval for `references/errors/` · branch protection · human PR review |
| Prompt-injection via task input | Trick the running agent into writing a poisoned `new_rule` that gets committed | Same as above; the lint-rules CI is best-effort, not airtight (see "Limitations" below) |
| Honest contributor pasting prod data | Leak PII / secrets into `error-log.md` | gitleaks pre-commit · explicit redaction reminder in `.github/ISSUE_TEMPLATE/error-capture.md` |

### Limitations

The CI rule validator (`tools/validate_rules.py`) is **best-effort, not airtight**:

- It allow-lists starting verbs and rejects an explicit set of forbidden patterns (URLs, shell binaries, credential paths, `<script>` tags, base64-shaped strings).
- It does not catch homoglyph attacks (`сurl` with Cyrillic с), indirection (`run "the {tool} command"`), or natural-language nudges that don't match any pattern.
- It is a static check, not a semantic check. **Human PR review remains the primary trust boundary.**

We have a 20-pattern adversarial test suite at `tests/test_validate_rules_adversarial.py` documenting which bypasses are caught and which are not. The current bypass-rate is documented honestly in that test file.

---

## Required GitHub branch-protection on `main`

To make the threat model effective, the repository owner must enable (Settings → Branches → Branch protection rules → `main`):

- **Require a pull request before merging** with at least 1 approving review.
- **Require status checks to pass before merging:** `lint-rules`, `ci / test (3.12, ubuntu)`.
- **Require branches to be up to date before merging.**
- **Require linear history** (squash-merge default).
- **Restrict who can push to matching branches** — including admins (this prevents accidental admin override).
- **Do not allow force pushes.**
- **Do not allow deletions.**
- **Require review from Code Owners** (uses `.github/CODEOWNERS`).

Required signed commits (`Require signed commits`) are **Phase 2** — they raise the barrier for external contributors and are deferred until the project has co-maintainers.

---

## Recovery runbook for secret leakage

If a secret (API key, JWT, customer ID, internal hostname, etc.) is committed to `references/errors/error-log.md` or anywhere else in the tree:

1. **`git revert` is not enough** — the secret remains in git history.
2. Rotate the leaked secret at its source immediately. This is the only fully effective mitigation.
3. Use `git filter-repo --invert-paths --path <file>` (or `--replace-text`) to rewrite history.
4. Force-push the rewritten branch and notify all forks / clones to re-clone (`git pull` will fail and show the divergence).
5. Open a [GitHub Security Advisory](https://github.com/sordi-ai/skill-everything/security/advisories/new) so downstream users get notified.

`git filter-repo` is not bundled with git — install via `pip install git-filter-repo`.
