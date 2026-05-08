# Sub-Skill: Review & Deployment-Prozess

**Zweck:** Verhindert Deployment-Unfälle und stellt sicher, dass Reviews mehr als Rubber-Stamping sind.
Konkrete Checklisten die der Agent vor jedem PR und Deployment durchläuft.

---

## PR-Review-Checkliste (Agent führt diese durch bevor er einen PR öffnet)

### Korrektheit
- [ ] Alle neuen Funktionen haben Tests
- [ ] Bestehende Tests laufen durch (`npm test` / `pytest` / etc.)
- [ ] Edge Cases abgedeckt: null/undefined, leere Arrays, negative Zahlen
- [ ] Keine TODO-Kommentare ohne zugehöriges Ticket

### Sicherheit
- [ ] Keine Secrets oder API-Keys im Code (auch nicht in Kommentaren)
- [ ] User-Input wird validiert bevor er in DB-Queries oder Shell-Befehle fließt
- [ ] Neue Endpunkte haben Authentifizierung/Autorisierung
- [ ] Keine `eval()`, `exec()`, oder dynamische SQL-Strings ohne Prepared Statements

### Performance
- [ ] Keine N+1-Queries (Datenbankabfragen in Schleifen)
- [ ] Große Datenmengen werden paginiert, nicht komplett geladen
- [ ] Neue Indizes für neue WHERE-Klauseln in Queries

### Wartbarkeit
- [ ] Komplexe Logik ist kommentiert (das *Warum*, nicht das *Was*)
- [ ] Keine duplizierten Code-Blöcke (DRY)
- [ ] Abhängigkeiten aktualisiert in `package.json` / `requirements.txt`

---

## Deployment-Checkliste

### Vor dem Deployment
1. **Migrations prüfen:** Sind alle DB-Migrations rückwärtskompatibel? (Kein DROP COLUMN ohne vorherigen Deprecation-Zyklus)
2. **Feature Flags:** Neue Features hinter Feature Flag? Besonders bei großen Änderungen.
3. **Rollback-Plan:** Wie wird zurückgerollt wenn etwas schiefläuft? Dokumentiert?
4. **Monitoring:** Sind Alerts für neue kritische Pfade eingerichtet?

### Deployment-Reihenfolge (bei Microservices)
1. Zuerst: Datenbankmigrationen (additive Änderungen)
2. Dann: Backend-Services (neue Version)
3. Zuletzt: Frontend (neue Version)
4. Niemals: Frontend vor Backend wenn API-Änderungen

### Nach dem Deployment
- [ ] Health-Check-Endpunkt antwortet mit 200
- [ ] Error-Rate in Monitoring nicht erhöht (5 Minuten beobachten)
- [ ] Kritische User-Flows manuell testen (Login, Hauptfunktion, Checkout)

---

## Eskalations-Regeln

| Situation | Aktion |
|-----------|--------|
| Test-Coverage fällt unter 70% | PR blockieren, Tests nachfordern |
| Security-Vulnerability in Dependency | Sofort patchen, kein Merge bis gefixt |
| Produktions-Fehler > 1% Error-Rate | Sofort rollback, dann analysieren |
| Deployment dauert > 30min | Abbrechen, Ursache suchen |

---

## Warum dieser Sub-Skill Sterne bringt

Der Agent vergisst nie die Sicherheits-Checks oder die Deployment-Reihenfolge.
Jeder PR ist production-ready bevor ein Mensch ihn sieht.
