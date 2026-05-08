# Sub-Skill: Fehler-Log

**Zweck:** Zentrales Gedächtnis für alle Fehler die der Agent gemacht hat oder beobachtet hat.
Jeder Eintrag verhindert, dass derselbe Fehler zweimal passiert.

---

## Format-Spezifikation

Jeder Fehler-Eintrag folgt exakt diesem YAML-Format:

```yaml
- id: ERR-YYYY-NNN          # Jahr + laufende Nummer, z.B. ERR-2025-001
  datum: YYYY-MM-DD
  last_seen: YYYY-MM-DD     # Letztes Auftreten (bei Wiederholung aktualisieren)
  count: 1                   # Wie oft dieser Fehler aufgetreten ist
  kategorie: development|git|deployment|security|performance|domain
  schwere: kritisch|hoch|mittel|niedrig
  kontext: |
    [1-3 Sätze: In welcher Situation ist der Fehler aufgetreten?
    Welche Aufgabe wurde bearbeitet? Welches Projekt/Modul?]
  was_passierte: |
    [Konkrete Beschreibung was der Agent getan hat.
    Code-Snippet wenn relevant.]
  root_cause: |
    [Warum ist es passiert? Welche falsche Annahme lag zugrunde?]
  auswirkung: |
    [Was war die Konsequenz? Datenverlust? Sicherheitslücke? Zeitverlust?]
  loesung: |
    [Was wurde getan um den Fehler zu beheben?]
  neue_regel: |
    [Die konkrete Regel die aus diesem Fehler folgt.
    Formuliert als Handlungsanweisung: "Immer X bevor Y" oder "Nie Z ohne W".]
  datei: references/[kategorie]/[dateiname].md   # Wo die Regel eingepflegt wurde
```

---

## Beispiel-Einträge

```yaml
fehler:

  - id: ERR-2025-001
    datum: 2025-03-14
    kategorie: deployment
    schwere: kritisch
    kontext: |
      Deployment einer neuen API-Version für den OrderFlow-Service.
      Die neue Version enthielt eine DB-Migration die eine Spalte umbenennt.
    was_passierte: |
      Agent hat zuerst das neue Backend deployed, dann die Migration ausgeführt.
      Zwischen Deployment und Migration (ca. 45 Sekunden) lief der neue Code
      gegen das alte Schema und warf 500-Fehler für alle Bestellungen.
    root_cause: |
      Falsche Annahme: "Migration kann nach Deployment laufen".
      Tatsächlich: Wenn Code neue Spalten-Namen erwartet, muss Migration ZUERST laufen.
    auswirkung: |
      45 Sekunden Produktionsausfall. ~200 fehlgeschlagene API-Requests.
      Kein Datenverlust, aber Kundenbeschwerden.
    loesung: |
      Sofort zurückgerollt auf alte Version. Migration ausgeführt.
      Dann neue Version deployed. Diesmal ohne Fehler.
    neue_regel: |
      Immer additive DB-Migrationen VOR dem Deployment ausführen.
      Bei Rename-Migrationen: Erst neue Spalte hinzufügen (additiv),
      Code auf neue Spalte umstellen, dann alte Spalte entfernen (separates Deployment).
    datei: references/process/review-deployment.md

  - id: ERR-2025-002
    datum: 2025-04-02
    kategorie: security
    schwere: kritisch
    kontext: |
      Implementierung eines neuen Such-Endpunkts für Produkte.
      Nutzer können nach Produktnamen suchen.
    was_passierte: |
      Agent hat folgende Query gebaut:
      ```sql
      SELECT * FROM products WHERE name LIKE '%' + userInput + '%'
      ```
      Direkte String-Konkatenation mit User-Input in SQL-Query.
    root_cause: |
      Fokus auf Funktionalität, Sicherheit nicht mitgedacht.
      Kein Prepared Statement verwendet.
    auswirkung: |
      SQL-Injection-Lücke. Angreifer könnte alle Daten auslesen oder löschen.
      Im Code-Review entdeckt, nie in Produktion.
    loesung: |
      Umgeschrieben mit Prepared Statement:
      ```sql
      SELECT * FROM products WHERE name LIKE ?
      ```
      Parameter: `%${userInput}%`
    neue_regel: |
      Nie User-Input direkt in SQL-Queries konkatenieren.
      Immer Prepared Statements oder ORM-Query-Builder verwenden.
      Vor jedem neuen Endpunkt: Checkliste "Sicherheit" aus review-deployment.md durchgehen.
    datei: references/process/review-deployment.md

  - id: ERR-2025-003
    datum: 2025-04-18
    kategorie: performance
    schwere: hoch
    kontext: |
      Feature: Dashboard zeigt alle Bestellungen eines Nutzers mit Produktdetails.
      Implementierung der Backend-API für das Dashboard.
    was_passierte: |
      Agent hat folgende Logik implementiert:
      ```typescript
      const orders = await db.orders.findAll({ where: { userId } });
      for (const order of orders) {
        order.items = await db.orderItems.findAll({ where: { orderId: order.id } });
        for (const item of order.items) {
          item.product = await db.products.findOne({ where: { id: item.productId } });
        }
      }
      ```
      Bei 50 Bestellungen mit je 5 Items: 1 + 50 + 250 = 301 DB-Queries.
    root_cause: |
      N+1-Query-Problem. Jede Ebene der Verschachtelung multipliziert die Queries.
      Kein JOIN oder eager loading verwendet.
    auswirkung: |
      Dashboard lädt 8 Sekunden statt <500ms.
      Datenbank unter Last bei mehreren gleichzeitigen Nutzern.
    loesung: |
      Umgeschrieben mit einem einzigen JOIN-Query:
      ```sql
      SELECT o.*, oi.*, p.*
      FROM orders o
      JOIN order_items oi ON oi.order_id = o.id
      JOIN products p ON p.id = oi.product_id
      WHERE o.user_id = ?
      ```
      Ladezeit: 45ms.
    neue_regel: |
      Vor jeder Implementierung die Daten aus DB lädt: Prüfen ob Schleifen mit
      DB-Calls drin sind. Wenn ja → JOIN oder Batch-Query verwenden.
      Faustregel: Maximal 1 DB-Query pro HTTP-Request (Ausnahmen dokumentieren).
    datei: references/development/code-quality.md
```

---

## Workflow: Fehler einpflegen

1. **Fehler erkennen:** Test schlägt fehl, Review-Kommentar, Produktionsfehler, oder Agent merkt selbst dass Ansatz falsch war.
2. **ID vergeben:** Nächste freie Nummer in diesem Jahr (`ERR-YYYY-NNN`).
3. **Eintrag ausfüllen:** Alle Felder, besonders `neue_regel` — das ist der Wert.
4. **Regel einpflegen:** Die `neue_regel` in die passende Datei unter `references/` einfügen.
5. **Commit:** `docs(errors): add ERR-2025-NNN - [kurze Beschreibung]`
