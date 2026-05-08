# Beitragen zu Skill-Everythink

Danke für dein Interesse! Skill-Everythink lebt von Community-Beiträgen — je mehr Wissen einfließt, desto besser werden die Agents für alle.

---

## Wie du beitragen kannst

### 1. Neuen Sub-Skill erstellen

1. Kopiere die Vorlage: `references/_templates/sub-skill.template.md`
2. Erstelle einen neuen Ordner unter `references/` oder nutze einen bestehenden
3. Benenne die Datei beschreibend: `references/[kategorie]/[thema].md`
4. Fülle mindestens 5 konkrete Regeln ein
5. Erstelle einen Pull Request

### 2. Bestehende Skills erweitern

1. Finde den passenden Sub-Skill in `references/`
2. Füge neue Regeln am Ende der passenden Kategorie ein
3. Format: `NNN. **[Regelname].** [Handlungsanweisung.]`
4. Wenn die Regel aus einem Fehler stammt: `Referenz: ERR-YYYY-NNN` anhängen

### 3. Fehler dokumentieren

1. Kopiere die Vorlage: `references/_templates/error-entry.template.md`
2. Fülle alle Felder aus
3. Füge den Eintrag in `references/errors/error-log.md` ein
4. Erstelle die zugehörige Regel im passenden Sub-Skill

---

## Konventionen

### Dateinamen
- Kleinbuchstaben, Bindestriche: `code-quality.md`, `review-deployment.md`
- Beschreibend, nicht abgekürzt: `conventions.md` statt `conv.md`

### Sprache
- Deutsch für Inhalte
- Englische Fachbegriffe sind OK: "Commit", "Pull Request", "Deploy"
- Regeln als Handlungsanweisungen: "Immer X" / "Nie Y ohne Z"

### Regeln
- Konkret und praxisnah — keine abstrakten Philosophien
- Mit Beispiel wenn möglich (Code-Snippet, konkreter Fall)
- Eine Regel pro Punkt — keine Doppelregeln

### Pull Requests
- Titel im Format: `docs([kategorie]): [was geändert wurde]`
- Beispiel: `docs(development): add React hook rules`
- Beschreibe kurz warum die Regel/der Skill wichtig ist
- Maximal ein Thema pro PR

---

## Ordnerstruktur

```
references/
├── development/     → Code-Qualität, Patterns, häufige Fehler
├── git/             → Commit-Konventionen, Branching, PRs
├── domain/          → Firmenwissen, Business-Regeln, Glossar
├── process/         → Reviews, Deployment, Checklisten
├── errors/          → Fehler-Log, Selbst-Erweiterungs-Workflow
└── _templates/      → Vorlagen für neue Skills und Fehler
```

Neue Kategorien sind willkommen! Erstelle einfach einen neuen Ordner mit einer `SKILL.md` oder thematischen `.md`-Datei.

---

## Was macht einen guten Beitrag aus?

✅ Konkrete Regeln aus echten Projekten
✅ Handlungsanweisungen statt Beschreibungen
✅ Fehler-Einträge mit Root-Cause-Analyse
✅ Domänenwissen das kein LLM von sich aus kennt

❌ Generische Tipps die in jeder Dokumentation stehen
❌ Persönliche Meinungen ohne Begründung
❌ Regeln ohne praktischen Mehrwert
