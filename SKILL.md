---
name: skill-everythink
description: Git-Versioned Agent Memory — Agents that never make the same mistake twice
version: 1.0.0
---

# Skill-Everythink

Du nutzt das **Skill-Everythink** Wissenssystem. Es enthält akkumuliertes Wissen aus vergangenen Fehlern, Projektkonventionen, Domänenwissen und Prozessen.

## Deine Pflichten

1. **Vor jeder Implementierung:** Prüfe ob relevante Sub-Skills existieren und lade sie via `skill_resource`.
2. **Nach jedem Fehler:** Führe den Selbst-Erweiterungs-Workflow aus (siehe unten).
3. **Bei neuem Wissen:** Pflege es in die passende Kategorie ein.

## Sub-Skill-Verzeichnis

Lade den passenden Sub-Skill wenn der Kontext zutrifft:

| Kontext | Sub-Skill | Laden via |
|---------|-----------|-----------|
| Code schreiben, refactoren, reviewen | Code-Qualität | `skill_resource(skill_name="skill-everythink", relative_path="references/development/code-quality.md")` |
| Git-Operationen, Commits, Branches, PRs | Git-Konventionen | `skill_resource(skill_name="skill-everythink", relative_path="references/git/conventions.md")` |
| Projektspezifisches Wissen benötigt | Domänenwissen | `skill_resource(skill_name="skill-everythink", relative_path="references/domain/template.md")` |
| PR erstellen, Deployment, Review | Review & Deployment | `skill_resource(skill_name="skill-everythink", relative_path="references/process/review-deployment.md")` |
| Einen Fehler gemacht / korrigiert | Fehler-Log | `skill_resource(skill_name="skill-everythink", relative_path="references/errors/error-log.md")` |

## Fehler-Einfang-Trigger

Starte den Selbst-Erweiterungs-Workflow wenn:

- Ein Test fehlschlägt wegen deinem Code
- Der User dich korrigiert ("Das war falsch", "Merk dir das")
- Du merkst dass dein erster Ansatz falsch war
- Ein Deployment-Problem auftritt

**Workflow laden:**
```
skill_resource(skill_name="skill-everythink", relative_path="references/errors/self-extension-workflow.md")
```

## Consolidation-Regel

Wenn `references/errors/error-log.md` mehr als 50 Einträge hat:
1. Ähnliche Fehler zusammenfassen (gleiche Root-Cause → ein Eintrag mit `count`)
2. Fehler die älter als 6 Monate sind und `schwere: niedrig` haben → archivieren
3. Regeln die daraus entstanden sind bleiben in den Sub-Skills erhalten

## Wichtig

- **Search before Write:** Bevor du einen neuen Fehler loggst, durchsuche das Error-Log nach ähnlichen Einträgen. Update statt Duplikat.
- **Handlungsanweisungen statt Beschreibungen:** Regeln immer als "Immer X bevor Y" oder "Nie Z ohne W" formulieren.
- **Kompakt bleiben:** Jeder Sub-Skill sollte unter 3000 Tokens bleiben. Bei Überschreitung → aufteilen.
