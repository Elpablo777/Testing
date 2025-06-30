
# MCP/Typescript/Python-SDK als Submodule

Hier können offizielle SDKs als Git-Submodule eingebunden werden:


```bash
# Python-SDK einbinden:
git submodule add https://github.com/modelcontextprotocol/python-sdk external/mcp-python-sdk
# Typescript-SDK einbinden:
git submodule add https://github.com/modelcontextprotocol/typescript-sdk external/mcp-typescript-sdk
```

**Status:**
- Noch keine SDK-Submodule eingebunden (Stand: 2025-06-30)
- Nach Ausführung der obigen Befehle erscheinen die SDKs als Unterordner und können direkt importiert werden.

**Beispielintegration (Python):**
```python
from external.mcp-python-sdk.mcp import Client
client = Client()
# ... weitere Nutzung siehe SDK-README ...
```

**Beispielintegration (Typescript):**
```typescript
import { Client } from './external/mcp-typescript-sdk';
const client = new Client();
// ... weitere Nutzung siehe SDK-README ...
```

**Hinweise:**
- Nach dem Klonen: `git submodule update --init --recursive`
- Siehe auch die README im jeweiligen SDK-Ordner für Installations- und Nutzungshinweise.
- Beispiel-Clients für MCP/A2A finden sich in `/tests/` und `/a2a-mcp/`.
