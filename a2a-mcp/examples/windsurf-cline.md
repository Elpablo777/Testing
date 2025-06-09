# Beispiel: Integration mit Windsurf, Cline & Co.

## MCP
- Nutze [python-sdk](https://github.com/modelcontextprotocol/python-sdk) oder [typescript-sdk](https://github.com/modelcontextprotocol/typescript-sdk) für direkten Zugriff auf das Model Context Protocol.
- Beispiel-Kontext-Nachricht: siehe context-schema.json

## A2A
- A2A-Nachrichtenstruktur: siehe a2a-message-example.json
- Für Orchestrierung (Windsurf): Agenten können Aufgaben per JSON an andere Agents übertragen.
- Für Cline: Kontext/Tasks/Resultate werden als standardisierte JSON-Nachrichten ausgetauscht.

## Tipp
- SDK als Dependency einbinden und eigene Agent-Methode nach Schema gestalten.