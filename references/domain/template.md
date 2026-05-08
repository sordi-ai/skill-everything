# Sub-Skill: Domänenwissen-Template

**Zweck:** Strukturiertes Template um firmen- oder projektspezifisches Wissen einzupflegen,
das kein öffentliches Modell kennen kann — Architektur-Entscheidungen, Naming-Konventionen, Business-Regeln.

---

## Anleitung: Dieses Template ausfüllen

Kopiere diese Datei nach `references/domain/<projektname>.md` und fülle alle Abschnitte aus.
Leere Abschnitte löschen. Konkret > vollständig.

---

## Projekt-Überblick

```
Projektname:     [z.B. "OrderFlow"]
Technologie:     [z.B. "Node.js 20, PostgreSQL 15, React 18"]
Deployment:      [z.B. "AWS ECS, GitHub Actions CI/CD"]
Team-Größe:      [z.B. "4 Backend, 2 Frontend"]
Haupt-Repo:      [z.B. "github.com/acme/orderflow"]
```

---

## Architektur-Entscheidungen (ADRs)

### ADR-001: [Titel]
- **Datum:** YYYY-MM-DD
- **Status:** Accepted / Deprecated / Superseded by ADR-XXX
- **Kontext:** Warum musste eine Entscheidung getroffen werden?
- **Entscheidung:** Was wurde entschieden?
- **Konsequenzen:** Was ändert sich dadurch?

---

## Naming-Konventionen

| Kontext | Konvention | Beispiel |
|---------|-----------|---------|
| Datenbank-Tabellen | snake_case, Plural | `order_items` |
| API-Endpunkte | kebab-case, Plural | `/api/order-items` |
| TypeScript-Interfaces | PascalCase, kein `I`-Prefix | `OrderItem` |
| Umgebungsvariablen | SCREAMING_SNAKE_CASE | `DATABASE_URL` |
| React-Komponenten | PascalCase | `OrderItemList` |

---

## Business-Regeln

> Diese Regeln sind nicht im Code dokumentiert — nur hier.

1. **[Regel-Name]:** [Beschreibung]. Beispiel: `Bestellungen unter 10€ haben keine Versandkosten.`
2. **[Regel-Name]:** [Beschreibung].

---

## Bekannte Fallstricke

1. **[Fallstrick]:** [Was passiert und warum]. Beispiel: `Die users-Tabelle hat zwei ID-Felder: id (intern) und external_id (Kundennummer). Nie verwechseln.`
2. **[Fallstrick]:** [Was passiert und warum].

---

## Externe Systeme & Integrationen

| System | Zweck | Auth-Methode | Kontakt bei Problemen |
|--------|-------|-------------|----------------------|
| Stripe | Zahlungen | API-Key in `STRIPE_SECRET_KEY` | payments@acme.com |
| SendGrid | E-Mails | API-Key in `SENDGRID_API_KEY` | devops@acme.com |

---

## Glossar

| Begriff | Bedeutung |
|---------|----------|
| `Order` | Eine bestätigte Bestellung (Status >= CONFIRMED) |
| `Cart` | Noch nicht bestätigte Bestellung (Status = DRAFT) |

---

## Agent-Direktiven

> Spezifische Anweisungen wie der Agent in diesem Projekt arbeiten soll.

1. **[Direktive]:** [Beschreibung]. Beispiel: `Lösche niemals Dateien ohne explizite Bestätigung des Users.`
2. **[Direktive]:** [Beschreibung]. Beispiel: `Gib bei jeder Änderung den vollständigen Dateipfad aus.`
3. **[Direktive]:** [Beschreibung]. Beispiel: `Nutze immer die deutsche Sprache in Commit-Messages.`

---

## Tech-Stack Quirks

> Eigenheiten des Stacks die nicht in der Dokumentation stehen — nur durch Erfahrung gelernt.

1. **[Quirk-Name]:** [Was passiert und warum]. Beispiel: `Prisma Client muss nach Schema-Änderungen mit npx prisma generate neu generiert werden — ein einfaches npm install reicht nicht.`
2. **[Quirk-Name]:** [Was passiert und warum]. Beispiel: `Der Redis-Connection-Pool in Produktion hat max. 10 Connections — bei mehr als 10 parallelen Requests gehen Requests verloren.`

---

## Warum dieser Sub-Skill Sterne bringt

Ohne Domänenwissen macht der Agent plausible aber falsche Annahmen über Naming, Business-Regeln und Architektur.
Mit diesem Template einmal ausgefüllt → der Agent kennt das Projekt wie ein Teammitglied.
