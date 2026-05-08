# Sub-Skill: Git & Workflow-Konventionen

**Zweck:** Einheitliche Commit-Historie, saubere Branches, keine Merge-Konflikte durch Disziplin.
Regeln die in Teams mit 2–20 Entwicklern funktionieren.

---

## Regeln

### Commit-Nachrichten (Conventional Commits)

1. **Format:** `<type>(<scope>): <beschreibung>` — immer Kleinbuchstaben, kein Punkt am Ende.
   - Typen: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`
   - Beispiel: `feat(auth): add JWT refresh token rotation`
2. **Beschreibung im Imperativ.** `add feature` nicht `added feature` oder `adds feature`.
3. **Scope ist der betroffene Modul-Name.** `fix(user-service): handle null email` — nicht `fix(backend)`.
4. **Breaking Changes mit `!` markieren.** `feat(api)!: remove deprecated v1 endpoints`
5. **Body bei nicht-offensichtlichen Änderungen.** Erklärt das *Warum*, nicht das *Was*.

### Branching

6. **Branch-Namen:** `<type>/<ticket-id>-<kurzbeschreibung>` — z.B. `feat/PROJ-123-user-export`.
7. **Feature-Branches leben max. 2 Tage.** Länger → täglich rebasen auf `main`.
8. **Kein direkter Push auf `main` oder `develop`.** Immer über Pull Request.
9. **Branch vor PR löschen.** Merged Branches im Remote aufräumen.

### Pull Requests

10. **PR-Titel = Commit-Nachricht des Squash-Commits.** Konsistenz zwischen PR und Git-Log.
11. **Max. 400 Zeilen Diff pro PR.** Größer → aufteilen. Reviewer können nicht mehr als 400 Zeilen sinnvoll reviewen.
12. **Self-Review vor PR-Öffnung.** Einmal selbst durchlesen, offensichtliche Fehler fixen.

### Merge-Strategie

13. **Squash-Merge für Feature-Branches.** Saubere lineare Historie auf `main`.
14. **Merge-Commit für Release-Branches.** Damit Release-Punkte sichtbar bleiben.
15. **`git rebase -i` vor PR für saubere Commits.** WIP-Commits zusammenfassen.

---

## Warum dieser Sub-Skill Sterne bringt

Der Agent erstellt automatisch korrekte Commit-Nachrichten und Branch-Namen.
Kein manuelles Nachkorrigieren, keine Diskussionen im Review über Formatierung.
