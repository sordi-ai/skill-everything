---
id: code-quality
version: 1.0.0
tokens_target: 1000
triggers:
  - writing code
  - refactoring
  - review
loads_after: []
supersedes: []
---

# Sub-Skill: Code Quality & Common Mistakes
<!-- target: ~1000 tokens (real tiktoken count, see tools/render_readme_table.py) | 23 rules -->

**Purpose:** Prevents the 20% of mistakes that cause 80% of review comments.
Concrete rules from real projects — no boilerplate.

---

## Rules

### Functions & Logic

1. **Functions max. 30 lines.** Longer → split. No exceptions for "complex logic".
2. **No boolean parameter as last argument.** `render(true)` is unreadable. Use enum or named object instead: `render({ withHeader: true })`.
3. **Early return instead of nested if-blocks.** Nesting depth > 2 is a warning sign.
4. **No magic numbers.** `if (status === 3)` → `if (status === OrderStatus.SHIPPED)`.
5. **No double negation.** `if (!isNotValid)` → `if (isValid)`.

### Variables & Naming

6. **Variable names describe content, not type.** `userList` instead of `arr`, `activeUserId` instead of `id`.
7. **Temporary variables for complex expressions.** `const isEligible = age >= 18 && !isBanned;` instead of cramming it all into an `if`.
8. **No abbreviations except established ones** (`id`, `url`, `ctx`, `req`, `res`). `usr`, `cfg`, `tmp` → spell them out.

### Error Handling

9. **Every `async` call needs a `try/catch` or `.catch()`.** Unhandled promise rejections crash Node processes.
10. **Never silently swallow error objects.** `catch (e) {}` is forbidden. At minimum: `logger.warn(e)`.
11. **Error messages must include context.** `throw new Error('User not found: ' + userId)` not `throw new Error('Not found')`.

### Imports & Dependencies

12. **No circular imports.** When in doubt: run `madge --circular src/`.
13. **External dependencies only in dedicated adapter files.** No direct `axios.get()` in business logic — always wrap through an interface.
14. **Remove `console.log` before commit.** Use a pre-commit hook or linter rule `no-console`.

### Tests

15. **Every new function needs at least one happy-path test.** No merge without test coverage for new logic.

### Performance

16. **No DB queries in loops (N+1 problem).** Instead of `for (item of items) { await db.find(item.id) }` → use a JOIN or `WHERE id IN (...)` query.
17. **Paginate large datasets.** Never `SELECT * FROM table` without `LIMIT`. API endpoints with lists need `?page=` and `?limit=`.
18. **New WHERE clauses need indexes.** Before every new query: is there a matching DB index? Without index → full table scan on growing data.
19. **Lazy loading for heavy operations.** Load data only when needed, not "just in case".

### Security

20. **Never use user input directly in queries.** Always use prepared statements or ORM query builders. Applies to SQL, NoSQL, shell commands, and template engines.
21. **New API endpoints need auth.** No endpoint without authentication and authorization — not even "internal" endpoints.
22. **Never put secrets in code.** No API keys, passwords, or tokens in source code or comments. Always use environment variables.
23. **Validate and sanitize user input.** At the system boundary (API entry): check type, length, format. Never trust blindly.

---

## Why This Sub-Skill Earns Stars

Without these rules, the agent produces code that works but immediately gets flagged in reviews.
With these rules, it writes code that looks like it came from a senior developer — on the first try.
