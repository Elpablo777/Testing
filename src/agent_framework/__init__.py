# Dieser Ordner enthält ein Framework zur Simulation von Multi-Agenten-Systemen.
# Basierend auf A2A/MCP-ähnlichen Nachrichten.

# Exportiere wichtige Klassen für einfacheren Zugriff
from .core.base_agent import BaseAgent
from .core.message_broker import MessageBroker

__all__ = ['BaseAgent', 'MessageBroker']
