
# Basis/Testing Repo

**Zweck:**  
Universelle, professionelle Startbasis für Projekte, Coding-Agenten, KI-Tools, alle Plattformen.

**Update- und Strukturhistory:**  
- Update-Logs im Ordner `/updates/`
- Strukturübersicht in `/docs/structure.md`

**Wichtige Ordner:**  
- `/src/`, `/tests/`, `/docs/` – Code, Tests, Doku
- `/web/`, `/mobile/`, `/pwa/` – Plattform-spezifisch
- `/lang/` – 20+ Sprachen
- `/frameworks/` – React, Flutter, Django, Express, PWA (Starthilfen)
- `/a2a-mcp/` – Agentenprotokolle MCP & A2A, Prompts, Beispiele, Integration
- `/logs/`, `/prompts/`, `/tasks/`, `/updates/` – Meta/Steuerung

**Schnittstellen/Kompatibilität:**
- **MCP:** Offizielle SDKs nutzen ([python](https://github.com/modelcontextprotocol/python-sdk), [typescript](https://github.com/modelcontextprotocol/typescript-sdk)), Beispiele & Schemata enthalten.
- **A2A:** JSON-basiertes Task- und Kontextprotokoll; Beispiele und Links enthalten.
- **Windsurf, Cline & Co:** Integration vorbereitet!
=======
>>>>>>> efe71c5 (Doku, Integrationsbeispiele, Community- und Feedback-Mechanismen, ToDo/Protokoll aktualisiert (30.06.2025))
**Checkliste:**  
- [x] Struktur & Basisdateien angelegt  
- [x] Update-Historie als einzelne Dateien  
- [x] Plattformen, Sprachen, Frameworks vorbereitet  
- [x] MCP/A2A sauber integriert & dokumentiert  
- [x] Eigene Beispiel-Clients und Submodule vorbereitet (siehe `/tests/`, `/external/`)
- [x] Agenten-Framework mit End-to-End-Workflow, Simulation und Testabdeckung

---

## Beispielablauf & Screenshots

**End-to-End-Agenten-Workflow (Ablaufdiagramm):**

![Ablaufdiagramm Agenten-Workflow](docs/assets/ablauf_agenten_workflow.png)

**Beispiel-Konsolenausgabe (Simulation):**

```shell
python3 src/agent_framework/run_agent_simulation.py
```

Beispiel-Output:
```text
UserProxyAgent: Anfrage empfangen: "Wie ist das Wetter in Berlin? Erstelle eine Datei mit dem Ergebnis."
TaskPlanningAgent: Zerlege Aufgabe in Teilaufgaben...
DataCollectionAgent: Hole Wetterdaten für Berlin...
LocalExecutionAgentInterface: Erstelle Datei mit Wetterdaten...
UserProxyAgent: Ergebnis an Nutzer zurückgegeben.
```

Weitere Screenshots und Beispielausgaben findest du in `docs/architektur_agenten.md` und `docs/quickstart_architektur.md`.

---


## Automatisierte Tests & CI

- Python-Tests: `python3 -m unittest discover -s tests/python`
- Node.js-Tests: `npx mocha tests/node/*.js`
- GitHub Actions: Automatische Checks bei jedem Commit (siehe `.github/workflows/ci.yml`)




## Hinweise für Feedback, Review & Community

- Feedback, Wünsche und Verbesserungsvorschläge sind ausdrücklich erwünscht! Am besten als GitHub-Issue oder per E-Mail (siehe CONTRIBUTING.md).
- Für Code-Reviews, Fragen und Diskussionen steht das Issue-Board zur Verfügung.
- Community-Richtlinien und Verhaltenskodex: Siehe `CODE_OF_CONDUCT.md`.
- Für Security-Reports: Siehe `SECURITY.md` (vertrauliche Meldung möglich).

- **End-to-End-Simulation:**
  - Siehe `src/agent_framework/run_agent_simulation.py` für einen vollständigen Beispielablauf ("Wetter in Berlin + Datei erstellen").
  - Nachrichtenfluss: UserProxyAgent → TaskPlanningAgent → DataCollectionAgent/LocalExecutionAgentInterface → zurück zum Nutzer.
  - Ablaufdiagramme und Nachrichtenformate: siehe `docs/architektur_agenten.md`.
  - **Tipp:** Für Präsentationen oder Doku können Screenshots der Diagramme und der Konsolenausgabe genutzt werden (siehe Beispiel in `docs/architektur_agenten.md`).

- **Automatisierte End-to-End-Tests:**
  - Siehe `tests/python/test_agent_e2e.py` für einen vollständigen Integrationstest aller Agentenrollen.
  - **Tipp:** Testausgaben können als Beispiel-Output in die Doku übernommen werden (z.B. als Codeblock oder Screenshot).

## Beispiel-Clients & SDK-Integration

- Python: Siehe `tests/python/test_mcp_client.py` (Platzhalter, echtes SDK empfohlen)
- Node.js: Siehe `tests/node/test_a2a_client.js` (Platzhalter)
- Submodule für MCP-SDKs können im Ordner `/external/` eingebunden werden (siehe `external/README.md`)

## Integrationsbeispiele (Windsurf, Cline, externe Plattformen)

- Siehe `a2a-mcp/windsurf-cline.md` für ein vollständiges Integrationsbeispiel (Ablauf, Beispiel-Nachricht, Adapter-Tipps).
- Für eigene Integrationen: Beispiel-Clients und Tests in `/tests/` als Vorlage nutzen.

---

*Letzte Version: v1.2.0 – siehe `/updates/v1.2.0.md`*