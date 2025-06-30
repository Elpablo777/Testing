# Integrationsbeispiel: Windsurf/Cline mit Agenten-Framework

Dieses Beispiel zeigt, wie das Agenten-Framework mit externen Plattformen wie Windsurf oder Cline integriert werden kann.

## Beispielablauf

1. **Windsurf/Cline** sendet eine Anfrage im MCP/A2A-Format an das Framework (z.B. via REST, WebSocket oder Datei).
2. Die Anfrage wird vom UserProxyAgent entgegengenommen und wie gewohnt verarbeitet.
3. Ergebnisse werden im passenden Format zurückgegeben (z.B. als JSON-Response oder Datei).

## Beispiel-Nachricht (A2A/MCP)
```json
{
  "sender": "windsurf-platform",
  "receiver": "agent-framework",
  "task_type": "data_collection",
  "payload": {
    "query": "Wetter in Hamburg"
  },
  "context": {
    "integration": "windsurf"
  },
  "timestamp": "2025-06-30T12:00:00Z"
}
```

## Hinweise zur Integration
- Für REST: Adapter/Proxy schreiben, der HTTP-Requests in Framework-Nachrichten übersetzt.
- Für Datei-Integration: Gemeinsames Verzeichnis für Nachrichten-JSONs nutzen.
- Für WebSocket: Direktes Forwarding der Nachrichten an den UserProxyAgent.


**Eigener Adapter: Vorlage (REST, Python, Pseudocode)**

```python
import requests

def windsuf_adapter(request_json):
    # Anfrage von Windsurf/Cline entgegennehmen (z.B. per REST-API)
    # Nachricht an UserProxyAgent weiterleiten (z.B. via Framework-API)
    response = send_to_agent_framework(request_json)
    # Antwort zurück an Windsurf/Cline
    return response

def send_to_agent_framework(msg):
    # Hier würde das eigentliche Agenten-Framework angesprochen (z.B. HTTP, direktes Python-Objekt, etc.)
    # Beispiel: requests.post('http://localhost:8000/agent', json=msg)
    return {"status": "ok", "result": "Demo-Antwort"}
```

**Tipp:**
- Die Beispiel-Clients und Tests in `/tests/` können als Vorlage für eigene Integrationsadapter dienen.
- Für weitere Beispiele siehe auch die offiziellen SDKs und die Doku der jeweiligen Plattform.
