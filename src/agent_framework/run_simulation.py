# Hauptskript zur Demonstration des simulierten Agenten-Frameworks.
# Dieses Skript initialisiert den MessageBroker, die verschiedenen Agenten
# und startet eine Beispielinteraktion, die verschiedene Szenarien abdeckt,
# einschließlich erfolgreicher Operationen und Fehlerbehandlung.

from core.message_broker import MessageBroker
# Importiere BaseAgent für den Fall, dass spezifische Rollen nicht direkt als Dummy genutzt werden
from core.base_agent import BaseAgent
from roles.user_proxy_agent import UserProxyAgent
from roles.task_planning_agent import TaskPlanningAgent
from roles.data_collection_agent import DataCollectionAgent
from roles.local_execution_agent_interface import LocalExecutionAgentInterface
import time # Wird für Pausen zwischen den Szenarien verwendet, um die Log-Ausgaben lesbarer zu machen.

def run_full_simulation():
    """
    Führt eine vollständige Simulation des Agenten-Workflows durch,
    inklusive Tests für neue command_types und Fehlerbehandlung.
    """
    print("=================================================================")
    print("=== STARTE ERWEITERTE AGENTEN-FRAMEWORK SIMULATION ===")
    print("=================================================================\n")

    # 1. MessageBroker initialisieren
    print("--- Initialisiere MessageBroker ---")
    broker = MessageBroker()
    print("MessageBroker initialisiert.\n")

    # 2. Agenten initialisieren und beim Broker registrieren
    print("--- Initialisiere Agenten ---")
    try:
        # UserProxyAgent: Nimmt Anfragen vom "Benutzer" entgegen und gibt finale Antworten aus.
        user_proxy = UserProxyAgent(
            agent_id="UserProxy_Sim",
            message_broker=broker,
            planning_agent_id="Planner_Sim" # ID des TaskPlanningAgent, an den Anfragen delegiert werden.
        )

        # DataCollectionAgent: Simuliert das Sammeln von Daten (z.B. Wetter, Aktien).
        data_collector = DataCollectionAgent(
            agent_id="Collector_Sim",
            message_broker=broker
        )

        # LocalExecutionAgentInterface: Simuliert die Ausführung lokaler Befehle (Dateien, Skripte).
        executor = LocalExecutionAgentInterface(
            agent_id="Executor_Sim",
            message_broker=broker,
            simulation_mode=True # Wichtig: Bleibt im sicheren Simulationsmodus.
        )

        # TaskPlanningAgent: Zerlegt Anfragen, delegiert an Collector oder Executor.
        planner = TaskPlanningAgent(
            agent_id="Planner_Sim",
            message_broker=broker,
            data_agent_id=data_collector.agent_id,
            exec_agent_id=executor.agent_id
        )

        print("\nAlle Agenten erfolgreich initialisiert und registriert:")
        print(f"  - {user_proxy}")
        print(f"  - {planner}")
        print(f"  - {data_collector}")
        print(f"  - {executor}")
        print("Registrierte Agenten im Broker:", broker.list_registered_agents())
        print("\n--- Agenten Initialisierung abgeschlossen ---\n")

    except Exception as e:
        print(f"FEHLER bei der Agenteninitialisierung: {e}")
        print("Stelle sicher, dass alle Agentenklassen korrekt implementiert sind und die __init__ Methoden stimmen.")
        return

    # --- Ab hier beginnen die verschiedenen Testszenarien ---

    # --- Szenario 1: Komplexe Anfrage an UserProxy (Wetter & Datei erstellen) ---
    # Ziel: Test des normalen Nachrichtenflusses über alle beteiligten Agenten.
    print("\n--- SZENARIO 1: Komplexe Anfrage (Wetter & Datei erstellen via UserProxy) ---")
    user_query_1 = "Informiere mich über das Wetter in Berlin und erstelle eine Python-Datei namens 'sim_output_1.py' mit dem Inhalt 'print(\"Szenario 1 erfolgreich!\")'."
    print(f"UserProxy startet Aufgabe mit Anfrage: \"{user_query_1}\"\n")
    try:
        user_proxy.initiate_task(user_query_1)
    except Exception as e:
        print(f"FEHLER bei Szenario 1 (initiate_task): {e}")
    print("-----------------------------------------------------------------\n")
    time.sleep(1) # Kurze Pause, um die (simulierte) asynchrone Verarbeitung abzuwarten.


    # --- Szenario 2: Direkte Aufgaben an LocalExecutionAgentInterface (Datei erstellen, dann lesen) ---
    # Ziel: Test der neuen command_types 'create_file' und 'read_file' und des simulierten Dateisystems.
    print("\n--- SZENARIO 2: Direkte Befehle an LocalExecutionAgentInterface (Erstellen & Lesen) ---")
    file_to_create_and_read = "meine_testdatei_szenario2.txt"
    file_content_original = "Dies ist ein Testinhalt für Szenario 2.\nZweite Zeile für die Datei."

    print(f"Sende 'create_file' für '{file_to_create_and_read}' direkt an Executor_Sim...\n")
    # Normalerweise würde der TaskPlanningAgent solche Nachrichten senden.
    # Hier senden wir direkt, um die Funktionalität des Executors isoliert zu testen.
    # Der UserProxy dient hier als technischer Absender der Nachricht.
    planner.send_message( # Planner sendet, um eine realistischere Kette zu haben
        receiver_id=executor.agent_id,
        task_type="execution_task",
        payload={
            "command_type": "create_file",
            "filename": file_to_create_and_read,
            "file_content": file_content_original
        },
        context={"original_request_id": "direct_exec_create_001", "description": "Szenario 2 - Datei erstellen"}
    )
    time.sleep(0.5)

    print(f"\nSende 'read_file' für '{file_to_create_and_read}' direkt an Executor_Sim...\n")
    planner.send_message(
        receiver_id=executor.agent_id,
        task_type="execution_task",
        payload={
            "command_type": "read_file",
            "filename": file_to_create_and_read
        },
        context={"original_request_id": "direct_exec_read_001", "description": "Szenario 2 - Datei lesen"}
    )
    # Die Antwort vom Executor (mit dem Dateiinhalt) wird in dessen handle_message geloggt
    # und an den Planner (Absender) gesendet, der sie ebenfalls loggen würde.
    print("-----------------------------------------------------------------\n")
    time.sleep(1)


    # --- Szenario 3: Fehlerprovokation - Anfrage an Planner, die zu Fehler bei Sub-Agent führt ---
    # Ziel: Testen, wie der TaskPlanningAgent mit einer error_response von einem Sub-Agenten umgeht.
    print("\n--- SZENARIO 3: Fehlerprovokation (Datenabfrage mit interner Fehlerchance oder unbekannter Query) ---")
    user_query_3 = "Suche nach dem aktuellen Preis für 'FantasiaCoin'." # Diese Query sollte der DataCollector nicht kennen.
    print(f"UserProxy startet Aufgabe mit Anfrage: \"{user_query_3}\"\n")
    try:
        user_proxy.initiate_task(user_query_3)
    except Exception as e:
        print(f"FEHLER bei Szenario 3 (initiate_task): {e}")
    print("-----------------------------------------------------------------\n")
    time.sleep(1)

    # --- Szenario 4: Fehlerprovokation - Ungültige Anfrage direkt an einen Agenten ---
    # Ziel: Testen der Payload-Validierung im LocalExecutionAgentInterface.
    print("\n--- SZENARIO 4: Fehlerprovokation (Ungültige execution_task an Executor - command_type fehlt) ---")
    print("Sende ungültige 'execution_task' (ohne command_type) direkt an Executor_Sim...\n")
    planner.send_message(
        receiver_id=executor.agent_id,
        task_type="execution_task",
        payload={ # Enthält keinen 'command_type'
            "filename": "ungueltig.txt",
            "details": "Dieser Task ist ungültig, da command_type fehlt."
        },
        context={"original_request_id": "direct_invalid_exec_001", "description": "Szenario 4 - Ungültiger Task"}
    )
    # Der Executor sollte eine error_response an den Planner (Absender) senden.
    print("-----------------------------------------------------------------\n")
    time.sleep(1)

    # --- Szenario 5: Nur Datensammlung (erfolgreich) ---
    # Ziel: Einfacher, erfolgreicher Durchlauf für eine reine Datenanfrage.
    print("\n--- SZENARIO 5: Nur Datensammlung (Aktienkurs via UserProxy) ---")
    user_query_5 = "Was ist der Aktienkurs von GME?" # Der DataCollector kennt "aktienkurs".
    print(f"UserProxy startet Aufgabe mit Anfrage: \"{user_query_5}\"\n")
    try:
        user_proxy.initiate_task(user_query_5)
    except Exception as e:
        print(f"FEHLER bei Szenario 5 (initiate_task): {e}")
    print("-----------------------------------------------------------------\n")
    time.sleep(1)

    # --- Szenario 6: Test von 'run_python_script' und 'execute_shell_command' direkt ---
    print("\n--- SZENARIO 6: Direkte Ausführung von Python-Skript und Shell-Befehl ---")
    print("Sende 'run_python_script' direkt an Executor_Sim...\n")
    planner.send_message(
        receiver_id=executor.agent_id,
        task_type="execution_task",
        payload={
            "command_type": "run_python_script",
            "script_code": "import platform\nprint(f'Hallo von Python auf {platform.system()}!')\nfor i in range(2):\n  print(f'Simulierte Iteration: {i+1}')"
        },
        context={"original_request_id": "direct_py_run_001"}
    )
    time.sleep(0.5)

    print("\nSende 'execute_shell_command' direkt an Executor_Sim...\n")
    planner.send_message(
        receiver_id=executor.agent_id,
        task_type="execution_task",
        payload={
            "command_type": "execute_shell_command",
            "shell_command": "ls -lart | grep 'simulated_file' || echo 'Keine simulierten Dateien gefunden mit grep'" # Beispielhafter Befehl
        },
        context={"original_request_id": "direct_shell_run_001"}
    )
    print("-----------------------------------------------------------------\n")
    time.sleep(1)

    # --- Überprüfung des simulierten Dateisystems am Ende ---
    if isinstance(executor, LocalExecutionAgentInterface):
        print("\n--- Endgültiger Zustand des simulierten Dateisystems (Executor_Sim) ---")
        files_in_sim_fs = executor.list_simulated_files()
        if files_in_sim_fs:
            print(f"Gefundene Dateien: {files_in_sim_fs}")
            for f_name in files_in_sim_fs:
                print(f"  --- Inhalt von '{f_name}' ---")
                print(executor.get_simulated_file_content(f_name))
                print(f"  --- Ende Inhalt von '{f_name}' ---")
        else:
            print("Das simulierte Dateisystem ist leer.")
        print("-----------------------------------------------------------------\n")


    print("\n=================================================================")
    print("=== AGENTEN-FRAMEWORK SIMULATION ABGESCHLOSSEN ===")
    print("=================================================================")

if __name__ == "__main__":
    run_full_simulation()
