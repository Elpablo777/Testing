import json

class MessageBroker:
    """
    Ein einfacher MessageBroker, der Nachrichten zwischen registrierten Agenten weiterleitet.
    Dies ist eine sehr rudimentäre Implementierung für Simulationszwecke.
    """
    def __init__(self):
        """
        Initialisiert den MessageBroker mit einem leeren Agentenverzeichnis.
        """
        self.agents = {} # Speichert Agenten-Instanzen mit ihrer ID als Schlüssel
        print("DEBUG: MessageBroker initialisiert.")

    def register_agent(self, agent):
        """
        Registriert einen Agenten beim Broker.

        Args:
            agent (BaseAgent): Die zu registrierende Agenteninstanz.

        Raises:
            ValueError: Wenn der Agent bereits registriert ist oder keine agent_id hat.
        """
        if not hasattr(agent, 'agent_id') or not agent.agent_id:
            raise ValueError("Agent muss eine 'agent_id' haben.")
        if agent.agent_id in self.agents:
            raise ValueError(f"Agent mit ID {agent.agent_id} ist bereits registriert.")

        self.agents[agent.agent_id] = agent
        print(f"DEBUG: Agent {agent.agent_id} beim MessageBroker registriert.")

    def unregister_agent(self, agent_id):
        """
        Deregistriert einen Agenten vom Broker.

        Args:
            agent_id (str): Die ID des zu deregistrierenden Agenten.
        """
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"DEBUG: Agent {agent_id} vom MessageBroker deregistriert.")
        else:
            print(f"WARNUNG: Versuch, nicht registrierten Agenten {agent_id} zu deregistrieren.")

    def route_message(self, message):
        """
        Leitet eine Nachricht an den empfangenden Agenten weiter.

        Args:
            message (dict): Die zu sendende Nachricht. Muss 'receiver' und 'sender' Schlüssel enthalten.

        Raises:
            ValueError: Wenn die Nachricht ungültig ist oder der Empfänger nicht registriert ist.
        """
        if not isinstance(message, dict):
            raise ValueError("Nachricht muss ein Dictionary sein.")

        receiver_id = message.get("receiver")
        sender_id = message.get("sender")
        message_id = message.get("message_id", "N/A")

        if not receiver_id:
            raise ValueError(f"Nachricht {message_id} von {sender_id} hat keinen Empfänger ('receiver').")
        if not sender_id:
            # Weniger kritisch, aber gut zu wissen
            print(f"WARNUNG: Nachricht {message_id} an {receiver_id} hat keinen Absender ('sender').")

        if receiver_id in self.agents:
            receiver_agent = self.agents[receiver_id]
            try:
                # Versuche, die Nachricht dem Empfänger-Agenten zuzustellen und ihn die Nachricht verarbeiten zu lassen.
                print(f"DEBUG: MessageBroker leitet Nachricht {message_id} von {sender_id} an {receiver_id} weiter.")
                receiver_agent.receive_message(message)
            except Exception as e:
                # Fängt alle Fehler ab, die während der `receive_message` oder `handle_message` Methode des Empfängeragenten auftreten.
                print(f"FEHLER: Kritischer Fehler im Agenten {receiver_id} bei der Verarbeitung von Nachricht {message_id} von {sender_id}. Fehler: {e}")
                # Zukünftige Erweiterung: Hier könnte eine Fehlernachricht an den ursprünglichen Sender gesendet werden
                # oder die Nachricht in eine "Dead Letter Queue" verschoben werden.
        else:
            # Der angegebene Empfänger-Agent ist nicht im Broker registriert.
            print(f"WARNUNG: Empfänger-Agent '{receiver_id}' für Nachricht {message_id} (gesendet von '{sender_id}') ist nicht registriert. Nachricht wird verworfen.")
            print(f"DETAIL: Verworfene Nachricht: {json.dumps(message, indent=2)}")
            # Zukünftige Erweiterung: Eine "Unzustellbar"-Nachricht könnte hier an den sender_id gesendet werden,
            # falls dieser existiert und registriert ist.

    def get_agent(self, agent_id):
        """
        Gibt die Instanz eines registrierten Agenten zurück.

        Args:
            agent_id (str): Die ID des gesuchten Agenten.

        Returns:
            BaseAgent oder None: Die Agenteninstanz oder None, wenn nicht gefunden.
        """
        return self.agents.get(agent_id)

    def list_registered_agents(self):
        """
        Listet die IDs aller registrierten Agenten auf.
        """
        return list(self.agents.keys())

if __name__ == '__main__':
    # Kleiner Test der Funktionalität
    from base_agent import BaseAgent

    broker = MessageBroker()

    # Test-Agenten erstellen und registrieren
    agent_alpha = BaseAgent(agent_id="Alpha", message_broker=broker)
    agent_beta = BaseAgent(agent_id="Beta", message_broker=broker)

    print("\nRegistrierte Agenten:", broker.list_registered_agents())

    # Alpha sendet eine Nachricht an Beta
    print("\nSende Testnachricht von Alpha an Beta...")
    agent_alpha.send_message(
        receiver_id="Beta",
        task_type="greeting",
        payload={"text": "Hallo Beta!"},
        context={"conversation_id": "conv123"}
    )

    # Beta überprüft sein Postfach (obwohl handle_message schon geloggt haben sollte)
    print("\nBetas Postfach überprüfen (sollte leer sein, da handle_message direkt verarbeitet):")
    beta_messages = agent_beta.check_inbox()
    if beta_messages:
        for msg in beta_messages:
            print(f"Beta hat im Postfach gefunden: {msg}")
    else:
        print("Betas Postfach ist wie erwartet leer.")

    # Test: Nachricht an einen nicht existierenden Agenten
    print("\nSende Testnachricht von Alpha an Gamma (nicht existent)...")
    agent_alpha.send_message(
        receiver_id="Gamma",
        task_type="ping",
        payload={}
    )

    print("\nMessageBroker Test abgeschlossen.")
