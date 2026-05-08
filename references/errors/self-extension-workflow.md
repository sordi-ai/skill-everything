# Selbst-Erweiterungs-Workflow

**Zweck:** Exakter Prompt und Ablauf den der Agent nach jedem Fehler ausführt,
um das Skill-System automatisch zu aktualisieren.

---

## Trigger-Bedingungen

Der Agent startet diesen Workflow wenn **eine** dieser Bedingungen zutrifft:

- Ein Test schlägt fehl und der Agent hat den falschen Code geschrieben
- Ein Code-Review-Kommentar korrigiert den Agent
- Der Agent merkt während der Implementierung, dass sein erster Ansatz falsch war
- Ein Deployment-Problem tritt auf das der Agent verursacht hat
- Der Nutzer sagt explizit: "Das war falsch" / "Das solltest du dir merken"

---

## Schritt-für-Schritt-Ablauf

### Schritt 0: Search before Write (PFLICHT)

**Bevor du einen neuen Fehler-Eintrag erstellst**, durchsuche das bestehende Error-Log:

```
1. Lies references/errors/error-log.md
2. Suche nach ähnlichen Fehlern (gleiche Kategorie + ähnlicher Kontext)
3. Wenn ein ähnlicher Eintrag existiert:
   → Erhöhe dessen `count` Feld um 1
   → Aktualisiere `last_seen` auf heute
   → Ergänze den Kontext falls nötig
   → Erstelle KEINEN neuen Eintrag
4. Nur wenn kein ähnlicher Eintrag existiert → weiter mit Schritt 1
```

### Schritt 1: Fehler analysieren

Der Agent stellt sich intern diese Fragen:

```
1. Was genau habe ich getan? (konkreter Code/Aktion)
2. Was hätte ich stattdessen tun sollen?
3. Warum habe ich es falsch gemacht? (falsche Annahme, fehlendes Wissen, Unachtsamkeit)
4. Welche Kategorie trifft zu?
   - development: Code-Fehler, falsche Implementierung
   - git: Commit/Branch-Fehler
   - deployment: Deployment-Reihenfolge, Konfiguration
   - security: Sicherheitslücke
   - performance: N+1, fehlende Indizes, zu große Datenmengen
   - domain: Falsches Verständnis von Business-Regeln
5. Wie schwer war der Fehler? (kritisch/hoch/mittel/niedrig)
```

### Schritt 2: Neue Fehler-ID bestimmen

```bash
# Letzten Eintrag in error-log.md finden
grep "id: ERR-" references/errors/error-log.md | tail -1
# Nächste Nummer nehmen: ERR-2025-004 → ERR-2025-005
```

### Schritt 3: Fehler-Eintrag formulieren

Der Agent füllt das Template aus `references/errors/error-log.md` aus.
**Kritisch:** Die `neue_regel` muss eine **Handlungsanweisung** sein, keine Beschreibung.

❌ Schlecht: `"SQL-Injection ist gefährlich"`
✅ Gut: `"Nie User-Input direkt in SQL konkatenieren. Immer Prepared Statements."`

### Schritt 4: Passende Ziel-Datei bestimmen

| Fehler-Kategorie | Ziel-Datei |
|-----------------|-----------|
| development | `references/development/code-quality.md` |
| git | `references/git/conventions.md` |
| deployment | `references/process/review-deployment.md` |
| security | `references/process/review-deployment.md` (Sicherheits-Abschnitt) |
| performance | `references/development/code-quality.md` (Performance-Abschnitt) |
| domain | `references/domain/<projektname>.md` |

### Schritt 5: Regel in Ziel-Datei einfügen

Die neue Regel wird am Ende des passenden Abschnitts eingefügt.
Format: `NNN. **[Kurzer Regelname]:** [Handlungsanweisung]. Referenz: ERR-YYYY-NNN`

Beispiel:
```markdown
16. **Kein direktes SQL mit User-Input:** Nie User-Input in SQL-Queries konkatenieren.
    Immer Prepared Statements oder ORM verwenden. Referenz: ERR-2025-002
```

### Schritt 6: Fehler-Eintrag in error-log.md einfügen

Neuen YAML-Block am Ende der `fehler:`-Liste in `references/errors/error-log.md` einfügen.

### Schritt 7: Committen

```bash
git add references/errors/error-log.md references/[kategorie]/[dateiname].md
git commit -m "docs(errors): add ERR-$(date +%Y)-NNN - [kurze Beschreibung des Fehlers]"
```

---

## Der konkrete Selbst-Erweiterungs-Prompt

Wenn der Agent einen Fehler erkennt, führt er intern diesen Prompt aus:

```
FEHLER-DOKUMENTATION STARTEN

Ich habe gerade einen Fehler gemacht. Ich dokumentiere ihn jetzt systematisch.

ANALYSE:
- Was ich getan habe: [konkrete Aktion/Code]
- Was ich hätte tun sollen: [korrekte Aktion/Code]  
- Warum ich es falsch gemacht habe: [root cause]
- Kategorie: [development|git|deployment|security|performance|domain]
- Schwere: [kritisch|hoch|mittel|niedrig]

NEUE REGEL (Handlungsanweisung):
"[Immer/Nie/Vor X immer Y] ..."

AKTIONEN:
1. Nächste freie ERR-ID aus error-log.md bestimmen
2. Vollständigen YAML-Eintrag in error-log.md einfügen
3. Neue Regel in [ziel-datei] am Ende des passenden Abschnitts einfügen
4. Beide Dateien committen mit: docs(errors): add [ERR-ID] - [beschreibung]

JETZT AUSFÜHREN.
```

---

## Beispiel: Vollständiger Durchlauf

**Situation:** Agent hat eine React-Komponente ohne `key`-Prop in einer Liste gerendert.
React zeigt Warning, Performance-Probleme bei Re-Renders.

**Schritt 1 — Analyse:**
```
Was getan: <li>{item.name}</li> in .map() ohne key-Prop
Was stattdessen: <li key={item.id}>{item.name}</li>
Warum falsch: key-Prop vergessen, kein Linter-Fehler weil ESLint nicht konfiguriert
Kategorie: development
Schwere: mittel
```

**Schritt 2 — ID:** Letzte ID war ERR-2025-003 → neue ID: ERR-2025-004

**Schritt 3 — Neue Regel:**
```
"Jedes .map() in React muss ein key-Prop haben. key = stabile eindeutige ID aus den Daten,
nie Array-Index (außer Liste ist statisch und nie umsortiert)."
```

**Schritt 4 — Ziel-Datei:** `references/development/code-quality.md` (development-Kategorie)

**Schritt 5 — Regel einfügen** in `code-quality.md`:
```markdown
16. **React list key-Prop:** Jedes `.map()` braucht `key={item.id}`.
    Nie Array-Index als key bei dynamischen Listen. Referenz: ERR-2025-004
```

**Schritt 6 — YAML-Eintrag** in `error-log.md` einfügen (vollständiges Format).

**Schritt 7 — Commit:**
```bash
git commit -m "docs(errors): add ERR-2025-004 - react list missing key prop"
```

---

## Qualitätskontrolle

Nach dem Einfügen prüft der Agent:

- [ ] Ist die `neue_regel` eine Handlungsanweisung (nicht nur eine Beschreibung)?
- [ ] Hat der Eintrag alle Pflichtfelder (id, datum, kategorie, schwere, kontext, was_passierte, root_cause, neue_regel)?
- [ ] Ist die Regel in der richtigen Ziel-Datei eingefügt?
- [ ] Ist der Commit mit korrektem Conventional-Commit-Format?
- [ ] Würde diese Regel denselben Fehler in Zukunft verhindern?

Wenn alle 5 Punkte ✅ → Workflow abgeschlossen.

---

## Consolidation-Loop (ab 50 Einträgen)

Wenn `references/errors/error-log.md` mehr als **50 Fehler-Einträge** enthält, führe nach dem normalen Workflow zusätzlich eine Konsolidierung durch:

### Regeln:
1. **Zusammenfassen:** Fehler mit gleicher `root_cause` und `kategorie` → in einen Eintrag mit `count: N` zusammenfassen
2. **Archivieren:** Fehler mit `schwere: niedrig` die älter als 6 Monate sind → in `references/errors/archive/` verschieben
3. **Regeln behalten:** Die daraus entstandenen Regeln in den Sub-Skills bleiben IMMER erhalten — nur der Error-Log-Eintrag wird archiviert
4. **Prüfen:** Sind alle Regeln in den Sub-Skills noch relevant? Veraltete Regeln markieren mit `(veraltet seit YYYY-MM-DD)`

### Wann prüfen:
- Nach jedem 10. neuen Fehler-Eintrag
- Oder wenn der User explizit "Fehler-Log aufräumen" sagt
