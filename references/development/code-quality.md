# Sub-Skill: Code-Qualität & häufige Fehler

**Zweck:** Verhindert die 20% der Fehler, die 80% der Review-Kommentare ausmachen.
Konkrete Regeln aus echten Projekten — kein Boilerplate.

---

## Regeln

### Funktionen & Logik

1. **Funktionen max. 30 Zeilen.** Länger → aufteilen. Keine Ausnahmen für "komplexe Logik".
2. **Kein Boolean-Parameter als letztes Argument.** `render(true)` ist unleserlich. Stattdessen Enum oder benanntes Objekt: `render({ withHeader: true })`.
3. **Early Return statt verschachtelter if-Blöcke.** Tiefe > 2 ist ein Warnsignal.
4. **Keine Magic Numbers.** `if (status === 3)` → `if (status === OrderStatus.SHIPPED)`.
5. **Keine doppelte Negation.** `if (!isNotValid)` → `if (isValid)`.

### Variablen & Benennung

6. **Variablennamen beschreiben Inhalt, nicht Typ.** `userList` statt `arr`, `activeUserId` statt `id`.
7. **Temporäre Variablen für komplexe Ausdrücke.** `const isEligible = age >= 18 && !isBanned;` statt alles in ein `if`.
8. **Keine Abkürzungen außer etablierten** (`id`, `url`, `ctx`, `req`, `res`). `usr`, `cfg`, `tmp` → ausschreiben.

### Fehlerbehandlung

9. **Jeder `async`-Aufruf hat ein `try/catch` oder `.catch()`.** Unbehandelte Promise-Rejections crashen Node-Prozesse.
10. **Fehler-Objekte nie stumm schlucken.** `catch (e) {}` ist verboten. Mindestens `logger.warn(e)`.
11. **Fehlermeldungen enthalten Kontext.** `throw new Error('User not found: ' + userId)` statt `throw new Error('Not found')`.

### Imports & Abhängigkeiten

12. **Keine zirkulären Imports.** Bei Verdacht: `madge --circular src/` ausführen.
13. **Externe Abhängigkeiten nur in dedizierten Adapter-Dateien.** Kein direktes `axios.get()` in Business-Logik — immer über ein Interface wrappen.
14. **`console.log` vor Commit entfernen.** Pre-commit Hook oder Linter-Regel `no-console`.

### Tests

15. **Jede neue Funktion mit mindestens einem Happy-Path-Test.** Kein Merge ohne Test-Coverage für neue Logik.

### Performance

16. **Keine DB-Queries in Schleifen (N+1-Problem).** Statt `for (item of items) { await db.find(item.id) }` → einen JOIN oder `WHERE id IN (...)` Query nutzen.
17. **Große Datenmengen paginieren.** Nie `SELECT * FROM table` ohne `LIMIT`. API-Endpunkte mit Listen brauchen `?page=` und `?limit=`.
18. **Neue WHERE-Klauseln brauchen Indizes.** Vor jeder neuen Query prüfen: Gibt es einen passenden DB-Index? Ohne Index → Full Table Scan bei wachsenden Daten.
19. **Lazy Loading für schwere Operationen.** Daten erst laden wenn sie gebraucht werden, nicht "auf Vorrat".

### Security

20. **Nie User-Input direkt in Queries.** Immer Prepared Statements oder ORM-Query-Builder. Gilt für SQL, NoSQL, Shell-Commands, und Template-Engines.
21. **Neue API-Endpunkte brauchen Auth.** Kein Endpunkt ohne Authentifizierung und Autorisierung — auch nicht "interne" Endpunkte.
22. **Secrets nie im Code.** Keine API-Keys, Passwörter, Tokens in Quellcode oder Kommentaren. Immer Umgebungsvariablen nutzen.
23. **User-Input validieren und sanitizen.** An der Systemgrenze (API-Eingang): Typ, Länge, Format prüfen. Nie blindes Vertrauen.

---

## Warum dieser Sub-Skill Sterne bringt

Ohne diese Regeln produziert der Agent Code, der zwar funktioniert aber in Reviews sofort auffällt.
Mit diesen Regeln schreibt er Code, der wie von einem Senior-Entwickler aussieht — beim ersten Versuch.
