# Sub-Skill: Review & Deployment Process

**Purpose:** Prevents deployment accidents and ensures reviews are more than rubber-stamping.
Concrete checklists the agent runs through before every PR and deployment.

---

## PR Review Checklist (Agent runs this before opening a PR)

### Correctness
- [ ] All new functions have tests
- [ ] Existing tests pass (`npm test` / `pytest` / etc.)
- [ ] Edge cases covered: null/undefined, empty arrays, negative numbers
- [ ] No TODO comments without a linked ticket

### Security
- [ ] No secrets or API keys in code (not even in comments)
- [ ] User input is validated before flowing into DB queries or shell commands
- [ ] New endpoints have authentication/authorization
- [ ] No `eval()`, `exec()`, or dynamic SQL strings without prepared statements

### Performance
- [ ] No N+1 queries (database queries in loops)
- [ ] Large datasets are paginated, not loaded entirely
- [ ] New indexes for new WHERE clauses in queries

### Maintainability
- [ ] Complex logic is commented (the *why*, not the *what*)
- [ ] No duplicated code blocks (DRY)
- [ ] Dependencies updated in `package.json` / `requirements.txt`

---

## Deployment Checklist

### Before Deployment
1. **Check migrations:** Are all DB migrations backward-compatible? (No DROP COLUMN without prior deprecation cycle)
2. **Feature flags:** New features behind a feature flag? Especially for large changes.
3. **Rollback plan:** How to roll back if something goes wrong? Documented?
4. **Monitoring:** Are alerts set up for new critical paths?

### Deployment Order (for microservices)
1. First: Database migrations (additive changes)
2. Then: Backend services (new version)
3. Last: Frontend (new version)
4. Never: Frontend before backend when there are API changes

### After Deployment
- [ ] Health check endpoint responds with 200
- [ ] Error rate in monitoring not elevated (observe for 5 minutes)
- [ ] Critical user flows manually tested (login, main feature, checkout)

---

## Escalation Rules

| Situation | Action |
|-----------|--------|
| Test coverage drops below 70% | Block PR, request additional tests |
| Security vulnerability in dependency | Patch immediately, no merge until fixed |
| Production errors > 1% error rate | Rollback immediately, then analyze |
| Deployment takes > 30 min | Abort, investigate root cause |

---

## Why This Sub-Skill Earns Stars

The agent never forgets security checks or deployment order.
Every PR is reviewed as if a senior developer went through the checklist — automatically.
