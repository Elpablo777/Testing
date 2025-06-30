# Simuliertes Agenten Framework

Dieses Framework dient zur Simulation eines Multi-Agenten-Systems, das auf Nachrichten basiert, ähnlich den Prinzipien von A2A (Agent-to-Agent) und MCP (Model Context Protocol). Es ermöglicht die Definition verschiedener Agenten-Rollen, deren Interaktion über einen zentralen `MessageBroker` und die Verarbeitung von Aufgaben durch Delegation.

## Kernkomponenten

-   **`core/`**: Enthält die grundlegenden Bausteine des Frameworks.
    -   `base_agent.py`: Definiert die `BaseAgent`-Klasse, von der alle spezifischen Agenten erben. Sie handhabt die Registrierung beim Broker und das Senden/Empfangen von Nachrichten.
    -   `message_broker.py`: Definiert die `MessageBroker`-Klasse, die für die Weiterleitung von Nachrichten zwischen den registrierten Agenten zuständig ist.
-   **`roles/`**: Enthält Implementierungen für spezifische Agenten-Rollen.
    -   `user_proxy_agent.py`: `UserProxyAgent` - Nimmt Anfragen vom (simulierten) Benutzer entgegen und gibt finale Ergebnisse aus.
    -   `task_planning_agent.py`: `TaskPlanningAgent` - Zerlegt komplexe Anfragen in Teilaufgaben, delegiert diese an spezialisierte Agenten und aggregiert die Ergebnisse.
    -   `data_collection_agent.py`: `DataCollectionAgent` - Simuliert die Beschaffung von Informationen (z.B. Wetterdaten, Suchergebnisse).
    -   `local_execution_agent_interface.py`: `LocalExecutionAgentInterface` - Simuliert die Ausführung von Code oder Systembefehlen. Dieser Agent wertet einen `command_type` in der an ihn gesendeten `execution_task`-Nachricht aus. Unterstützte `command_types` sind aktuell:
        -   `create_file`: Erstellt (simuliert) eine Datei. Benötigt `filename` und optional `file_content` in der Payload.
        -   `read_file`: Liest (simuliert) den Inhalt einer Datei. Benötigt `filename`. Das Ergebnis enthält den gelesenen `file_content`.
        -   `run_python_script`: Simuliert die Ausführung eines Python-Skripts. Benötigt `script_code`.
        -   `execute_shell_command`: Simuliert die Ausführung eines Shell-Befehls. Benötigt `shell_command`.
        Er dient als Schnittstelle zu einem potenziellen, lokal laufenden Ausführungsagenten (z.B. Open Interpreter).
-   **`message_examples/`**: Enthält JSON-Beispiele für die Nachrichtenformate, die zwischen den Agenten ausgetauscht werden. Diese illustrieren die Struktur von Anfragen, Aufgaben und Ergebnissen (siehe z.B. `planning_delegation_exec_example.json` für ein Beispiel mit `command_type`).

## Funktionsweise

1.  **Initialisierung**:
    -   Eine Instanz des `MessageBroker` wird erstellt.
    -   Instanzen der benötigten Agenten (abgeleitet von `BaseAgent`) werden erstellt und dabei dem `MessageBroker` übergeben, der sie registriert.
2.  **Nachrichtenaustausch**:
    -   Agenten senden Nachrichten über ihre `send_message`-Methode.
    -   Der `MessageBroker` empfängt diese Nachricht und leitet sie an den im Nachrichten-Header spezifizierten Empfänger-Agenten weiter, indem er dessen `receive_message`-Methode aufruft.
    -   Jeder Agent implementiert eine `handle_message`-Methode, um auf spezifische Nachrichtentypen und Aufgaben zu reagieren.
3.  **Aufgabenverarbeitung (Beispielhafter Fluss)**:
    -   Ein `UserProxyAgent` erhält eine Anfrage (z.B. vom Benutzer).
    -   Er sendet eine `user_request`-Nachricht an den `TaskPlanningAgent`.
    -   Der `TaskPlanningAgent` analysiert die Anfrage, zerlegt sie ggf. in Teilaufgaben und sendet entsprechende `task`-Nachrichten (z.B. `data_collection_task`, `execution_task`) an spezialisierte Agenten (`DataCollectionAgent`, `LocalExecutionAgentInterface`).
    -   Die spezialisierten Agenten führen ihre (simulierten) Aufgaben aus und senden `result`-Nachrichten (z.B. `data_collection_result`, `execution_result`) zurück an den `TaskPlanningAgent`.
    -   Sobald der `TaskPlanningAgent` alle Ergebnisse für die ursprüngliche Anfrage erhalten hat, fasst er diese zusammen und sendet eine `final_response`-Nachricht an den `UserProxyAgent`.
    -   Der `UserProxyAgent` stellt das Ergebnis dar.

## Verwendung (Simulation)

Um eine Simulation zu starten:

1.  Importiere die benötigten Agentenklassen und den `MessageBroker`.
2.  Erstelle eine `MessageBroker`-Instanz.
3.  Erstelle und registriere Instanzen der Agenten.
4.  Starte eine Interaktion, z.B. indem der `UserProxyAgent` eine Aufgabe initiiert.

Ein Beispielskript `run_simulation.py` (wird noch erstellt) im Hauptverzeichnis dieses Frameworks wird einen vollständigen Durchlauf demonstrieren.

## Anbindung an reale Systeme

Während dieses Framework primär für die Simulation gedacht ist, können die definierten Nachrichtenformate und die Agentenlogik als Blaupause für die Interaktion mit realen Systemen dienen. Beispielsweise könnte der `LocalExecutionAgentInterface` so erweitert werden, dass er tatsächlich mit Tools wie Open Interpreter kommuniziert, um Befehle auf dem lokalen System auszuführen (mit entsprechenden Sicherheitsvorkehrungen).

## Zukünftige Erweiterungen

-   Komplexere Logik zur Aufgabenzerlegung im `TaskPlanningAgent` (z.B. durch Anbindung eines LLM).
-   Persistentere Speicherung von Nachrichten oder Agentenzuständen.
-   Asynchrone Nachrichtenverarbeitung.
-   Erweiterte Fehlerbehandlung und Resilienz.
-   Dynamische Registrierung/Deregistrierung von Agenten.
