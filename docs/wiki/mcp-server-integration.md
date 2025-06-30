# MCP-Server/Context7-Integration

## Ziel
- Anbindung des Agenten-Frameworks an einen lokalen oder gehosteten MCP-Server (z.B. context7.com)
- Beispiel-Workflow: Agenten-Framework <-> MCP-Server <-> externer Client
- Doku, Beispiel-Config, Testskripte und Integrationshinweise

## Voraussetzungen
- MCP-Server (lokal oder remote, z.B. https://context7.com/ oder https://github.com/modelcontextprotocol/servers)
- Python/Node.js-Client (siehe /tests/)
- Agenten-Framework (dieses Repo)

## Beispiel-Workflow
1. Externer Client sendet eine MCP/A2A-Nachricht an den MCP-Server
2. MCP-Server leitet die Nachricht an das Agenten-Framework weiter (z.B. per REST, WebSocket, Datei)
3. Das Framework verarbeitet die Aufgabe und sendet das Ergebnis zurück an den MCP-Server
4. Der MCP-Server gibt das Ergebnis an den Client zurück

## Beispiel-Konfiguration
```json
{
  "server_url": "https://context7.com/api/v1/",
  "framework_endpoint": "http://localhost:8000/agent",
  "auth_token": "<TOKEN>"
}
```

## Beispielcode (Python, Pseudocode)
```python
import requests

def send_task_to_mcp(task):
    url = "https://context7.com/api/v1/tasks"
    headers = {"Authorization": "Bearer <TOKEN>"}
    response = requests.post(url, json=task, headers=headers)
    return response.json()

# Beispiel-Aufruf
result = send_task_to_mcp({"task": "Wetter in Berlin"})
print(result)
```

## Hinweise
- Siehe https://github.com/modelcontextprotocol/servers für eigene Server-Instanz
- Für lokale Tests: Docker-Image oder Python-Server nutzen
- Testskripte und Beispiel-Clients im Ordner /tests/
- Feedback und Erfahrungen bitte als Issue dokumentieren!
