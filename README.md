# 🧠 Skill-Everythink
**Agents that never make the same mistake twice.**

Git-Versioned Agent Memory — Der intelligente Feintuning-Ersatz.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![GitHub Stars](https://img.shields.io/github/stars/sordi-ai/skill-everythink?style=social)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

---

## 🤔 Warum Skill-Everythink? Das Problem

Fine-Tuning ist teuer, zeitaufwändig und liefert ein starres Modell, das nach dem Training nichts mehr dazulernt. RAG löst das Wissensproblem, erfordert aber Vektorinfrastruktur, Embeddings und laufende Wartung. Cursor Rules sind statisch, nicht versioniert und funktionieren nur in Cursor — kein anderer Agent profitiert davon. Systeme wie mem0 oder MemGPT sind mächtig, aber opaque: Man weiß nicht, was gespeichert wurde, warum, und wie es sich auf das Verhalten auswirkt.

Das Kernproblem bleibt überall gleich: **Kein Agent lernt aus seinen Fehlern.** Derselbe Fehler passiert morgen wieder — in einem anderen Projekt, mit einem anderen Nutzer, auf einem anderen Rechner.

---

## ✅ Die Lösung

Skill-Everythink ist ein Git-versioniertes Gedächtnissystem aus Plain-Markdown-Dateien:

- **Plain Markdown** — keine Datenbank, kein Framework, kein Lock-in
- **Git-versioniert** — jede Änderung ist nachvollziehbar, revertierbar, reviewbar
- **Fehler-Gedächtnis** — Fehler werden analysiert, als Regel formuliert und dauerhaft gespeichert
- **Domänenwissen** — Firmenprozesse, Konventionen, Partner-Infos fließen strukturiert ein
- **Agent-agnostisch** — funktioniert mit OpenCode, Cursor, Claude, GPT-4, jedem LLM-basierten Agent
- **Modular** — Sub-Skills sind unabhängig, kombinierbar, einzeln ladbar
- **Kein Setup** — `git clone` und fertig, keine Infrastruktur nötig
- **Transparent** — jeder kann lesen, was der Agent weiß und warum

---

## 🚀 Quick-Start

**Schritt 1: Repository klonen**

```bash
git clone https://github.com/sordi-ai/skill-everythink.git
```

**Schritt 2: Skill in deinen Agent laden**

```bash
# OpenCode — in opencode.json oder als Skill-Pfad
"skills": ["./skill-everythink/SKILL.md"]

# Cursor — in .cursorrules oder Settings > Rules
@file:./skill-everythink/SKILL.md

# Claude (API / Projects) — als System-Prompt-Anhang
<skill src="./skill-everythink/SKILL.md" />
```

**Schritt 3: Fertig.**

Dein Agent hat jetzt Gedächtnis. Er kennt deine Konventionen, erinnert sich an vergangene Fehler und erweitert sein Wissen bei jedem neuen Einsatz.

---

## ⚙️ Wie es funktioniert

### Der Lernkreislauf

```
Agent macht Fehler
       ↓
Fehler wird analysiert (Ursache, Kontext, Auswirkung)
       ↓
Regel wird formuliert ("Tue X nie ohne Y zu prüfen")
       ↓
Skill wird aktualisiert (references/errors/ oder passendes Sub-Modul)
       ↓
Agent macht den Fehler nie wieder — in keinem Projekt
```

### Nicht nur Fehler

Der Kreislauf gilt für jede Art von Wissen:

- **Neue Erkenntnisse** — bessere Patterns, effizientere Ansätze
- **Prozesse** — Deployment-Schritte, Review-Checklisten, Onboarding-Flows
- **Konventionen** — Namensgebung, Commit-Stil, Architekturentscheidungen
- **Partner-Infos** — API-Eigenheiten, externe Systeme, Integrationsfallen

Jedes Mal, wenn der Agent etwas Wichtiges lernt, landet es im Skill — strukturiert, versioniert, sofort verfügbar.

---

## 📊 Vergleichstabelle

| Feature | Fine-Tuning | RAG | Cursor Rules | **Skill-Everythink** |
|---|---|---|---|---|
| Kosten | Hoch (GPU, Zeit) | Mittel (Infra) | Gering | **Minimal** |
| Lernt aus Fehlern | Nein | Nein | Nein | **Ja** |
| Git-versioniert | Nein | Nein | Optional | **Ja** |
| Agent-agnostisch | Nein | Teilweise | Nein (Cursor only) | **Ja** |
| Kein Setup nötig | Nein | Nein | Ja | **Ja** |
| Domänenwissen | Begrenzt | Ja | Begrenzt | **Ja** |
| Modular | Nein | Teilweise | Nein | **Ja** |
| Transparent | Nein | Teilweise | Ja | **Ja** |

---

## 📁 Projektstruktur

```
skill-everythink/
├── SKILL.md                    # Router — Einstiegspunkt (wird immer geladen)
├── references/
│   ├── development/            # Code-Qualität (15 Regeln)
│   ├── git/                    # Commit-Konventionen (15 Regeln)
│   ├── domain/                 # Firmenwissen-Template
│   ├── process/                # Review & Deployment
│   ├── errors/                 # Fehler-Log + Selbst-Erweiterung
│   └── _templates/             # Vorlagen für neue Skills
├── docs/                       # Präsentation & Erklärungen
├── CONTRIBUTING.md             # Wie man beiträgt
└── LICENSE                     # MIT
```

`SKILL.md` ist der zentrale Einstiegspunkt. Er wird immer geladen und entscheidet, welche Sub-Skills für die aktuelle Aufgabe relevant sind. Sub-Skills in `references/` sind eigenständige Module — sie können einzeln, kombiniert oder vollständig geladen werden.

---

## 📦 Mitgelieferte Starter-Skills

| Sub-Skill | Beschreibung |
|---|---|
| `references/development/` | 15 Regeln für sauberen, wartbaren Code — von Namensgebung bis Fehlerbehandlung |
| `references/git/` | 15 Regeln für konsistente Commit-Nachrichten, Branch-Strategien und PR-Hygiene |
| `references/domain/` | Template für firmenspezifisches Wissen: Systeme, Prozesse, Ansprechpartner |
| `references/process/` | Checklisten für Code-Review, Deployment und Incident-Response |
| `references/errors/` | Strukturiertes Fehler-Log mit Analyse, Regel und Präventions-Maßnahme |

---

## 🔄 Selbst-Erweiterung

Der Agent kann seinen eigenen Skill erweitern — ohne menschliches Eingreifen. So funktioniert der Workflow:

1. **Trigger** — Der Agent erkennt einen Fehler, eine neue Erkenntnis oder eine fehlende Regel
2. **Analyse** — Ursache, Kontext und Auswirkung werden strukturiert erfasst
3. **Formulierung** — Eine klare, handlungsrelevante Regel wird formuliert (präzise, nicht vage)
4. **Einordnung** — Die Regel wird dem passenden Sub-Skill zugeordnet (`errors/`, `development/`, etc.)
5. **Eintrag** — Der Agent schreibt den Eintrag in die entsprechende Markdown-Datei
6. **Commit** — Die Änderung wird per Git committet — mit Kontext, Datum und Begründung

Das Ergebnis: Ein Skill, der mit jedem Einsatz besser wird — nachvollziehbar, revertierbar, reviewbar.

---

## 🛠️ Eigenen Skill erstellen

**Schritt 1: Template kopieren**

```bash
cp references/_templates/skill-template.md references/mein-bereich/SKILL.md
```

**Schritt 2: Template ausfüllen**

Trage Kontext, Regeln und Beispiele ein. Halte jeden Sub-Skill unter 3000 Tokens — lieber aufteilen als aufblähen.

**Schritt 3: PR erstellen**

```bash
git checkout -b feat/mein-skill
git add references/mein-bereich/
git commit -m "feat(skills): add mein-bereich skill"
git push origin feat/mein-skill
```

Dann Pull Request auf GitHub öffnen. Details und Review-Kriterien in [./CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 🗺️ Roadmap

- **v1.0** — Core System + 5 Starter-Skills ← *aktuell*
- **v1.1** — CLI-Tool (`npx skill-everythink init`) für schnelles Projekt-Setup
- **v1.2** — Consolidation-Loop (automatisches Zusammenführen ähnlicher Regeln) + GitHub Actions Linter
- **v2.0** — Skill-Marketplace: Community-Skills entdecken, bewerten und direkt einbinden

---

## ❓ FAQ

**Funktioniert das mit meinem Agent?**
Ja. Skill-Everythink ist vollständig agent-agnostisch. Solange dein Agent Markdown-Dateien als Kontext laden kann — ob als System-Prompt, Datei-Referenz oder Skill-Konfiguration — funktioniert es. Getestet mit OpenCode, Cursor, Claude Projects, GPT-4 und lokalen Modellen via Ollama.

**Wie groß darf ein Skill werden?**
Pro Sub-Skill maximal 3000 Tokens. Das ist die Grenze, ab der Kontext-Overhead und Aufmerksamkeitsverlust spürbar werden. Wenn ein Bereich wächst, teile ihn in zwei fokussierte Sub-Skills auf — lieber zwei präzise Module als ein aufgeblähtes.

**Kann der Agent den Skill wirklich selbst erweitern?**
Ja. Der Selbst-Erweiterungs-Workflow in `references/errors/` beschreibt exakt, wie der Agent neue Einträge formuliert, einordnet und committet. Der Mensch reviewt den PR — der Agent schreibt ihn.

**Was ist der Unterschied zu `.cursorrules`?**
Cursor Rules sind statisch, nicht versioniert und funktionieren nur in Cursor. Skill-Everythink ist modular, Git-versioniert, agent-agnostisch und hat ein aktives Fehler-Gedächtnis. Ein Skill wächst mit — eine `.cursorrules`-Datei nicht.

**Brauche ich eine Datenbank?**
Nein. Alles ist Plain Markdown, gespeichert im Dateisystem, versioniert mit Git. Keine Vektordatenbank, kein Embedding-Service, kein laufender Prozess. `git clone` ist das einzige Setup.

**Kann ich Skill-Everythink in einem bestehenden Projekt verwenden?**
Ja. Klone das Repository neben dein Projekt oder füge es als Git-Submodul ein. Der Skill-Pfad wird einmalig in der Agent-Konfiguration eingetragen — danach läuft alles automatisch.

**Was passiert, wenn ein Skill-Eintrag falsch ist?**
`git revert`. Jede Änderung ist versioniert und kann in Sekunden rückgängig gemacht werden. Das ist einer der Kernvorteile gegenüber opaquen Speichersystemen.

---

## 🤝 Contributing

Beiträge sind willkommen — ob neue Starter-Skills, Verbesserungen bestehender Regeln oder Tooling. Bitte lies zuerst [./CONTRIBUTING.md](./CONTRIBUTING.md).

---

## 📄 Lizenz

MIT — frei verwendbar, modifizierbar und verteilbar, auch kommerziell. Siehe [LICENSE](./LICENSE).
