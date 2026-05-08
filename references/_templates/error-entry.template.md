# Fehler-Eintrag Template

Kopiere diesen Block und fülle alle Felder aus:

```yaml
  - id: ERR-YYYY-NNN
    datum: YYYY-MM-DD
    last_seen: YYYY-MM-DD
    count: 1
    kategorie: development|git|deployment|security|performance|domain
    schwere: kritisch|hoch|mittel|niedrig
    kontext: |
      [1-3 Sätze: Situation, Aufgabe, Modul]
    was_passierte: |
      [Was genau der Agent getan hat. Code-Snippet wenn relevant.]
    root_cause: |
      [Warum es passiert ist. Welche falsche Annahme?]
    auswirkung: |
      [Konsequenz: Datenverlust? Ausfall? Zeitverlust?]
    loesung: |
      [Was wurde getan um den Fehler zu beheben?]
    neue_regel: |
      [Handlungsanweisung: "Immer X bevor Y" oder "Nie Z ohne W".]
    datei: references/[kategorie]/[dateiname].md
```

## Checkliste vor dem Einfügen

- [ ] Ist ein ähnlicher Fehler bereits im Error-Log? → Update statt neuer Eintrag
- [ ] Ist `neue_regel` eine Handlungsanweisung (nicht nur Beschreibung)?
- [ ] Wurde die Regel in die passende Ziel-Datei eingefügt?
- [ ] Ist die nächste freie ERR-ID korrekt?
