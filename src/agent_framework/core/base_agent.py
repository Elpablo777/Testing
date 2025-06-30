import json
import time
import uuid

class BaseAgent:
    """
    Eine Basisklasse für einen Agenten in einem simulierten Multi-Agenten-System.
    Jeder Agent hat eine eindeutige ID und kann Nachrichten senden und empfangen
    über einen MessageBroker.
    """
    def __init__(self, agent_id, message_broker):
        """
        Initialisiert den Agenten.

        Args:
            agent_id (str): Eine eindeutige ID für den Agenten.
            message_broker (MessageBroker): Die Instanz des MessageBrokers,
                                           über den Nachrichten gesendet und empfangen werden.
        """
        if not agent_id:
            raise ValueError("Agent ID darf nicht leer sein.")
        if message_broker is None:
            raise ValueError("MessageBroker darf nicht None sein.")

        self.agent_id = agent_id
        self.message_broker = message_broker
        self.message_broker.register_agent(self)
        self.inbox = [] # Einfache Liste als Posteingang

    def send_message(self, receiver_id, task_type, payload, context=None):
        """
        Erstellt und sendet eine Nachricht an einen anderen Agenten über den MessageBroker.

        Args:
            receiver_id (str): Die ID des empfangenden Agenten.
            task_type (str): Der Typ der Aufgabe oder Nachricht (z.B. 'user_request', 'data_collection_task').
            payload (dict): Die eigentlichen Daten der Nachricht.
            context (dict, optional): Zusätzliche Kontextinformationen. Defaults to None.

        Returns:
            str: Die ID der gesendeten Nachricht.
        """
        if not receiver_id:
            raise ValueError("Receiver ID darf nicht leer sein.")
        if not task_type:
            raise ValueError("Task Type darf nicht leer sein.")

        message = {
            "sender": self.agent_id,
            "receiver": receiver_id,
            "message_id": f"msg_{uuid.uuid4()}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "task_type": task_type,
            "payload": payload or {},
            "context": context or {}
        }
        print(f"DEBUG: Agent {self.agent_id} sendet Nachricht {message['message_id']} an {receiver_id} (Typ: {task_type})")
        self.message_broker.route_message(message)
        return message["message_id"]

    def receive_message(self, message):
        """
        Wird vom MessageBroker aufgerufen, wenn eine Nachricht für diesen Agenten ankommt.
        Fügt die Nachricht dem Posteingang hinzu und ruft die handle_message Methode auf.

        Args:
            message (dict): Die empfangene Nachricht.
        """
        print(f"DEBUG: Agent {self.agent_id} hat Nachricht {message.get('message_id')} von {message.get('sender')} empfangen.")
        self.inbox.append(message)
        self.handle_message(message)

    def handle_message(self, message):
        """
        Verarbeitet eine empfangene Nachricht. Diese Methode sollte von abgeleiteten
        Agentenklassen überschrieben werden, um spezifische Logik zu implementieren.

        Args:
            message (dict): Die zu verarbeitende Nachricht.
        """
        # Standardimplementierung: Loggt die Nachricht.
        # In Unterklassen überschreiben, um auf Nachrichten zu reagieren.
        # Diese Methode wird von `receive_message` aufgerufen.
        try:
            # Die eigentliche Verarbeitungslogik sollte in den abgeleiteten Klassen implementiert werden.
            # Hier wird nur geloggt, dass die Basis-handle_message erreicht wurde, falls eine Unterklasse sie nicht überschreibt
            # oder super().handle_message() aufruft.
            print(f"INFO: {self.agent_id} - Basis-handle_message für Nachricht {message.get('message_id')} von {message.get('sender')}.")
            print(f"DETAIL: Nachrichteninhalt: {json.dumps(message, indent=2, ensure_ascii=False)}")

            # Hier ist der Platz, wo abgeleitete Agenten ihre spezifische Logik implementieren.
            # Wenn eine abgeleitete Klasse diese Methode nicht korrekt implementiert oder einen Fehler hat,
            # wird der folgende Except-Block ausgelöst.

        except Exception as e:
            # Fängt alle unerwarteten Fehler ab, die in der `handle_message`-Implementierung
            # einer abgeleiteten Agentenklasse auftreten könnten.
            print(f"FEHLER: Kritischer Fehler in Agent {self.agent_id} bei der spezifischen Verarbeitung (handle_message) von Nachricht {message.get('message_id')}.")
            print(f"FEHLERDETAILS: {e}")
            print(f"NACHRICHT, DIE ZUM FEHLER FÜHRTE: {json.dumps(message, indent=2, ensure_ascii=False)}")
            # Zukünftige Erweiterung: Hier könnte der Agent versuchen, eine standardisierte Fehlernachricht
            # an den ursprünglichen Absender der problematischen Nachricht oder an einen Supervisor-Agenten zu senden.
            # Beispiel:
            # if message.get("sender"):
            #     self.send_message(
            #         receiver_id=message.get("sender"),
            #         task_type="error_processing_message",
            #         payload={
            #             "error_summary": f"Fehler bei der Verarbeitung von Nachricht {message.get('message_id')}",
            #             "error_details": str(e),
            #             "original_message": message
            #         },
            #         context={"original_request_id": message.get("context", {}).get("original_request_id") or message.get("message_id")}
            #     )

    def check_inbox(self):
        """
        Gibt alle Nachrichten im Posteingang zurück und leert ihn.
        (Alternative zur direkten Verarbeitung in handle_message, falls ein Agent Nachrichten sammeln soll)
        """
        messages = list(self.inbox)
        self.inbox = []
        return messages

    def __str__(self):
        return f"Agent(id='{self.agent_id}')"

    def __repr__(self):
        return f"BaseAgent(agent_id='{self.agent_id}', message_broker={self.message_broker})"
