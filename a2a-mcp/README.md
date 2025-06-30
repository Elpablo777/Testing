# A2A & MCP – Agenten-Kommunikation & Model Context Protocol

## Was ist das?
- **MCP (Model Context Protocol)**: Offener Standard zur Kontext- und Aufgabenkommunikation zwischen KI-Modellen, Agenten, Apps.  
  - Offizielle Doku & Spezifikation: [modelcontextprotocol/modelcontextprotocol](https://github.com/modelcontextprotocol/modelcontextprotocol)
  - SDKs (empfohlen):  
    - [Python](https://github.com/modelcontextprotocol/python-sdk)
    - [TypeScript](https://github.com/modelcontextprotocol/typescript-sdk)
    - Weitere Tools: [Servers](https://github.com/modelcontextprotocol/servers), [Inspector](https://github.com/modelcontextprotocol/inspector)
  - Quickstart & Beispiele: [quickstart-resources](https://github.com/modelcontextprotocol/quickstart-resources)
- **A2A (Agent-to-Agent, Google)**: Offener Standard für Interoperabilität von KI-Agenten, v.a. über JSON für Tasks, Kontext, Ergebnisse.
  - Hintergrund: [Google A2A](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
  - Weitere Infos: [A2A Protocol Blog](https://a2aprotocol.ai/blog/a2a-travel-planner-openrouter)
  - Überblick, Prinzipien, Beispiele in [revolgy.com](https://www.revolgy.com/insights/blog/building-business-applications-with-google-cloud-ai-agent-tools)

## Integration in dieses Repo
- **Beispielschema** für MCP (siehe `context-schema.json`)
- **Beispiel-Nachricht** für A2A (siehe `a2a-message-example.json`)
- System/Prompts für Agentenkoordination im Unterordner `/prompts/`
- Für echte Integration: Offizielle SDKs als Submodule oder direkt im Projekt einbinden!

## Einsatz mit Windsurf, Cline, etc.
- Dieses Repo ist als universelle Brücke und Template für agentenbasierte Entwicklung vorbereitet.
- Für Code-Agents oder Orchestrierungsplattformen einfach die Schnittstellen/Prompts anpassen und die SDKs importieren.

## Weiterführende ToDos
- Eigene Beispiel-Clients bauen (siehe tasks/)
- Submodule für SDKs optional direkt einbinden (siehe ToDos)
- Integrationsbeispiele für spezifische Agentenplattformen ergänzen

## Beispiel- und Test-Clients

- Beispiel-Client für MCP (Python): `tests/python/test_mcp_client.py` (Platzhalter, für echte Nutzung SDK einbinden)
- Beispiel-Client für A2A (Node.js): `tests/node/test_a2a_client.js` (Platzhalter, für echte Nutzung SDK einbinden)
- Beispiel-Nachrichten: `a2a-message-example.json`, weitere Formate siehe `docs/architektur_agenten.md`

**Hinweise:**
- Für echte Integration: Offizielle SDKs als Submodule einbinden (siehe `/external/README.md`).
- Test- und Beispiel-Clients sind kommentiert und können als Vorlage für eigene Experimente dienen.
- Für Integrationsbeispiele mit Windsurf/Cline: Siehe ToDo-Liste und `/tasks/`.

## Anbindung an das interne Agenten-Framework
Dieses Repository enthält nun unter `src/agent_framework/` ein einfaches, simuliertes Framework für Multi-Agenten-Systeme. Dieses Framework nutzt die hier definierten A2A/MCP-ähnlichen Nachrichtenprinzipien zur Kommunikation zwischen simulierten Agenten mit verschiedenen Rollen (z.B. Planung, Datensammlung, Ausführung).

Das Framework dient als:
-   **Blaupause**: Wie komplexere Agenten-Interaktionen strukturiert werden können.
-   **Testumgebung**: Um Kommunikationsflüsse und Nachrichtenformate zu erproben.
-   **Ausgangspunkt**: Für die Entwicklung von anspruchsvolleren Agenten-Systemen, die möglicherweise reale lokale Tools (wie Open Interpreter) oder externe LLMs einbinden.

Weitere Details und eine Anleitung zur Nutzung finden Sie in der `README.md` des Frameworks unter [`src/agent_framework/README.md`](../src/agent_framework/README.md).

---