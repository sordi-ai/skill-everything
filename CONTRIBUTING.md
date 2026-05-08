# Contributing to Skill-Everythink

Thank you for your interest! Skill-Everythink thrives on community contributions — the more knowledge flows in, the better agents become for everyone.

---

## How You Can Contribute

### 1. Create a New Sub-Skill

1. Copy the template: `references/_templates/sub-skill.template.md`
2. Create a new folder under `references/` or use an existing one
3. Name the file descriptively: `references/[category]/[topic].md`
4. Fill in at least 5 concrete rules
5. Open a Pull Request

### 2. Extend Existing Skills

1. Find the matching sub-skill in `references/`
2. Add new rules at the end of the appropriate category
3. Format: `NNN. **[Rule Name].** [Action directive.]`
4. If the rule originates from an error: append `Reference: ERR-YYYY-NNN`

### 3. Document an Error

1. Copy the template: `references/_templates/error-entry.template.md`
2. Fill in all fields
3. Add the entry to `references/errors/error-log.md`
4. Create the corresponding rule in the appropriate sub-skill

---

## Conventions

### File Names
- Lowercase with hyphens: `code-quality.md`, `review-deployment.md`
- Descriptive, not abbreviated: `conventions.md` instead of `conv.md`

### Language
- English for all content
- Technical terms are fine as-is: "Commit", "Pull Request", "Deploy"
- Always phrase rules as action directives: "Always X before Y" or "Never Z without W"

### Rules
- Concrete and practical — no abstract philosophies
- Include an example where possible (code snippet, concrete case)
- One rule per point — never combine multiple rules into one

### Pull Requests
- Title format: `docs([category]): [what was changed]`
- Example: `docs(development): add React hook rules`
- Briefly describe why the rule or skill matters
- Always limit a PR to one topic

---

## Folder Structure

```
references/
├── development/     → Code quality, patterns, common mistakes
├── git/             → Commit conventions, branching, PRs
├── domain/          → Company knowledge, business rules, glossary
├── process/         → Reviews, deployment, checklists
├── errors/          → Error log, self-extension workflow
└── _templates/      → Templates for new skills and errors
```

> New categories are welcome! Simply create a new folder with a `SKILL.md` or a thematic `.md` file.

---

## What Makes a Good Contribution?

✅ Concrete rules from real projects  
✅ Action directives instead of descriptions  
✅ Error entries with root-cause analysis  
✅ Domain knowledge that no LLM would know by default  

❌ Generic tips found in any documentation  
❌ Personal opinions without justification  
❌ Rules without practical value  
