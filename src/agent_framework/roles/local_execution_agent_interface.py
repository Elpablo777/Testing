from ..core.base_agent import BaseAgent
import time
import random
import os # Obwohl nicht direkt genutzt in Simulation, deutet es auf potenzielle reale Nutzung hin
import json

class LocalExecutionAgentInterface(BaseAgent):
    """
    Ein Agent, der (simuliert) Aufgaben zur Code-Ausführung oder Systeminteraktion
    entgegennimmt. Wertet 'command_type' aus, um spezifische Aktionen zu simulieren.
    """
    def __init__(self, agent_id, message_broker, simulation_mode=True):
        super().__init__(agent_id, message_broker)
        self.simulation_mode = simulation_mode
        # Simuliertes Dateisystem für Dateioperationen im Simulationsmodus.
        # Format: { "dateiname.ext": "Dateiinhalt" }
        self.simulated_filesystem = {}
        print(f"LocalExecutionAgentInterface {self.agent_id} initialisiert. Simulationsmodus: {self.simulation_mode}")

    def handle_message(self, message):
        """
        Verarbeitet eingehende Nachrichten. Erwartet 'execution_task' mit einem 'command_type'.
        Simuliert die Ausführung basierend auf dem command_type und sendet das Ergebnis
        oder eine Fehlermeldung zurück.
        """
        # Ruft die Basisimplementierung auf (Logging und generelle Fehlerbehandlung durch BaseAgent)
        super().handle_message(message)

        msg_task_type = message.get("task_type")
        msg_sender = message.get("sender")
        msg_id = message.get("message_id")
        original_request_id = message.get("context", {}).get("original_request_id")
        payload = message.get("payload") # Payload wird hier schon geholt für Fehlerbehandlung

        try:
            if msg_task_type == "execution_task":
                # Überprüfung der Payload auf Existenz und Typ
                if not payload or not isinstance(payload, dict):
                    error_summary = f"Ungültige oder fehlende Payload in 'execution_task' von Agent {msg_sender}."
                    # ... (Fehlerbehandlung wie zuvor)
                    self.send_message(receiver_id=msg_sender,task_type="error_response",
                        payload={"error_summary": error_summary, "error_code": "ERR_INVALID_PAYLOAD",
                                 "error_details": f"Payload war: {json.dumps(payload, ensure_ascii=False)}",
                                 "original_message_id": msg_id},
                        context={"original_request_id": original_request_id})
                    return

                command_type = payload.get("command_type")
                if not command_type:
                    error_summary = f"Fehlendes 'command_type'-Feld in 'execution_task' von Agent {msg_sender}."
                    # ... (Fehlerbehandlung wie zuvor)
                    self.send_message(receiver_id=msg_sender, task_type="error_response",
                        payload={"error_summary": error_summary, "error_code": "ERR_MISSING_COMMAND_TYPE",
                                 "error_details": f"Payload war: {json.dumps(payload, ensure_ascii=False)}",
                                 "original_message_id": msg_id},
                        context={"original_request_id": original_request_id})
                    return

                print(f"INFO ({self.agent_id}): Erhielt execution_task mit command_type '{command_type}' von {msg_sender} (Nachricht ID: {msg_id}).")

                # Simulation der Ausführung mit kurzer Verzögerung
                time.sleep(random.uniform(0.1, 0.3))

                status = "failure" # Standardmäßig fehlschlagen, falls keine Logik zutrifft
                output_log = f"Aktion für command_type '{command_type}' gestartet."
                errors = ""
                # Dictionary für zusätzliche, befehlsspezifische Felder im Ergebnis-Payload.
                result_payload_extension = {}

                if self.simulation_mode:
                    # --- Beginn der Logik für verschiedene command_types ---
                    if command_type == "create_file":
                        filename = payload.get("filename")
                        file_content = payload.get("file_content", "") # Default ist leerer Inhalt
                        if filename:
                            self.simulated_filesystem[filename] = file_content
                            status = "success"
                            output_log += f"\nSimulierte Datei '{filename}' erfolgreich erstellt/überschrieben."
                            result_payload_extension = {"filename_processed": filename, "content_length": len(file_content)}
                            if random.random() < 0.05: # 5% simulierte Fehlerchance
                                status = "failure"
                                errors = f"Simulierter Fehler beim Erstellen der Datei '{filename}'."
                                if filename in self.simulated_filesystem: del self.simulated_filesystem[filename]
                        else:
                            errors = "'filename' fehlt für command_type 'create_file'."
                            output_log += f"\nFehler: Dateiname nicht spezifiziert für 'create_file'."

                    elif command_type == "read_file":
                        filename = payload.get("filename")
                        if filename:
                            if filename in self.simulated_filesystem:
                                status = "success"
                                file_content_read = self.simulated_filesystem[filename]
                                output_log += f"\nSimulierter Inhalt der Datei '{filename}' erfolgreich gelesen."
                                result_payload_extension = {"filename_processed": filename, "file_content": file_content_read, "content_length": len(file_content_read)}
                            else:
                                errors = f"Simulierte Datei '{filename}' nicht gefunden."
                                output_log += f"\nFehler: Datei '{filename}' existiert nicht im simulierten System."
                        else:
                            errors = "'filename' fehlt für command_type 'read_file'."
                            output_log += f"\nFehler: Dateiname nicht spezifiziert für 'read_file'."

                    elif command_type == "run_python_script":
                        script_code = payload.get("script_code")
                        if script_code:
                            status = "success"
                            output_log += f"\nSimulierte Ausführung von Python-Code erfolgreich.\n--- Code Snippet ---\n{script_code[:150]}{'...' if len(script_code)>150 else ''}\n--- (Simulierte Ausgabe) ---"
                            result_payload_extension = {"executed_code_snippet": script_code[:100] + ("..." if len(script_code) > 100 else "")}
                            if random.random() < 0.1: # 10% simulierte Fehlerchance
                                status = "failure"
                                errors = "Simulierter Fehler während der Python-Skriptausführung."
                        else:
                            errors = "'script_code' fehlt für command_type 'run_python_script'."
                            output_log += f"\nFehler: Kein Python-Code zur Ausführung übergeben."

                    elif command_type == "execute_shell_command":
                        shell_command = payload.get("shell_command")
                        if shell_command:
                            status = "success"
                            output_log += f"\nSimulierte Ausführung des Shell-Befehls: '{shell_command}' erfolgreich.\n(Simulierte Ausgabe für Shell-Befehl)"
                            result_payload_extension = {"executed_shell_command": shell_command}
                            if random.random() < 0.08: # 8% simulierte Fehlerchance
                                status = "failure"
                                errors = f"Simulierter Fehler bei der Ausführung des Shell-Befehls '{shell_command}'."
                        else:
                            errors = "'shell_command' fehlt für command_type 'execute_shell_command'."
                            output_log += f"\nFehler: Kein Shell-Befehl zur Ausführung übergeben."
                    else:
                        # Unbekannter command_type
                        errors = f"Unbekannter 'command_type': {command_type}."
                        output_log += f"\nFehler: Der Befehlstyp '{command_type}' wird nicht unterstützt."
                    # --- Ende der Logik für verschiedene command_types ---
                else: # Nicht im Simulationsmodus
                    errors = "Echte Ausführung ist in diesem Interface nicht implementiert und nicht erlaubt."
                    output_log += "\nKeine Aktion durchgeführt, da im Nicht-Simulationsmodus und keine echte Implementierung vorhanden."
                    status = "failure"

                # Zusammenstellen der Antwort-Payload
                response_payload = {
                    "command_type_processed": command_type,
                    "status": status,
                    "output_summary": output_log.split('\n')[0],
                    "full_output_log": output_log,
                    "error_details": errors,
                }
                response_payload.update(result_payload_extension) # Hinzufügen befehlsspezifischer Ergebnisse

                self.send_message(
                    receiver_id=msg_sender,
                    task_type="execution_result",
                    payload=response_payload,
                    context={"original_request_id": original_request_id, "delegated_task_id": msg_id}
                )
                print(f"INFO ({self.agent_id}): execution_result für command_type '{command_type}' an {msg_sender} gesendet (Status: {status}).")

            else: # Falls msg_task_type nicht "execution_task" ist
                print(f"WARNUNG ({self.agent_id}): Unerwarteter Nachrichtentyp '{msg_task_type}' von {msg_sender} (Nachricht ID: {msg_id}). Nachricht wird ignoriert.")

        except Exception as e:
            # Fängt alle anderen unerwarteten Fehler innerhalb der `handle_message`-Logik dieses Agenten ab.
            print(f"FEHLER ({self.agent_id}): Schwerwiegender interner Fehler bei der Verarbeitung der Nachricht {msg_id} von {msg_sender}. Fehler: {e}")
            if msg_sender: # Nur wenn ein Absender bekannt ist
                self.send_message(
                    receiver_id=msg_sender,
                    task_type="error_response",
                    payload={
                        "error_summary": f"Schwerwiegender interner Fehler im Agenten {self.agent_id} bei der Bearbeitung Ihrer Ausführungsanfrage.",
                        "error_code": "ERR_EXEC_AGENT_INTERNAL_FAILURE",
                        "error_details": str(e),
                        "original_message_id": msg_id,
                        "command_type_attempted": payload.get("command_type", "Unbekannt") if isinstance(payload, dict) else "Unbekannt"
                    },
                    context={"original_request_id": original_request_id}
                )

    def get_simulated_file_content(self, filename):
        """
        Gibt den Inhalt einer simulierten Datei zurück, falls vorhanden.
        Abhängigkeit: `self.simulation_mode` muss True sein.

        Args:
            filename (str): Der Name der simulierten Datei.

        Returns:
            str oder None: Der Inhalt der Datei oder None, wenn nicht gefunden oder nicht im Simulationsmodus.
        """
        if self.simulation_mode:
            return self.simulated_filesystem.get(filename)
        return None

    def list_simulated_files(self):
        """
        Listet die Namen aller Dateien im simulierten Dateisystem auf.
        Abhängigkeit: `self.simulation_mode` muss True sein.

        Returns:
            list[str]: Eine Liste der Dateinamen oder eine leere Liste.
        """
        if self.simulation_mode:
            return list(self.simulated_filesystem.keys())
        return []

if __name__ == '__main__':
    from ..core.message_broker import MessageBroker
    from ..core.base_agent import BaseAgent # Für den Dummy Planner

    broker = MessageBroker()
    # Dummy-Agent, der als Planer fungiert, um Aufgaben an den Executor zu senden.
    dummy_planner = BaseAgent("DummyPlanner_ExecTest_New", broker)
    executor = LocalExecutionAgentInterface("Executor_Test_New", broker, simulation_mode=True)

    print("\n--- LocalExecutionAgentInterface Testläufe (mit command_types und Fehlerbehandlung) ---")

    # TESTFALL 1: Valide 'create_file' Aufgabe
    print("\n--- TESTFALL 1: Valide 'create_file' Aufgabe ---")
    payload_create = {
        "command_type": "create_file",
        "filename": "mein_test_dokument.txt",
        "file_content": "Dies ist der Inhalt des Testdokuments.\nZweite Zeile."
    }
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_create, {"original_request_id": "exec_req_001"})
    # Direkte Überprüfung des simulierten Dateisystems nach der Operation.
    print(f"Simulierte Dateien nach Test 1: {executor.list_simulated_files()}")
    print(f"Inhalt von '{payload_create['filename']}':\n{executor.get_simulated_file_content(payload_create['filename'])}\n")

    # TESTFALL 2: Valide 'read_file' Aufgabe für eine existierende Datei
    print("\n--- TESTFALL 2: Valide 'read_file' Aufgabe (existierende Datei) ---")
    payload_read_exists = {"command_type": "read_file", "filename": "mein_test_dokument.txt"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_read_exists, {"original_request_id": "exec_req_002"})

    # TESTFALL 3: 'read_file' für eine nicht existierende Datei
    print("\n--- TESTFALL 3: 'read_file' Aufgabe (nicht existierende Datei) ---")
    payload_read_not_exists = {"command_type": "read_file", "filename": "gibts_nicht.txt"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_read_not_exists, {"original_request_id": "exec_req_003"})

    # TESTFALL 4: Valide 'run_python_script' Aufgabe
    print("\n--- TESTFALL 4: Valide 'run_python_script' Aufgabe ---")
    payload_run_python = {
        "command_type": "run_python_script",
        "script_code": "print('Hallo von Python!')\na = 10\nb = 20\nprint(f'Summe von a und b ist: {a+b}')"
    }
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_run_python, {"original_request_id": "exec_req_004"})

    # TESTFALL 5: Valide 'execute_shell_command' Aufgabe
    print("\n--- TESTFALL 5: Valide 'execute_shell_command' Aufgabe ---")
    payload_run_shell = {"command_type": "execute_shell_command", "shell_command": "echo 'Hallo Shell!' && date"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_run_shell, {"original_request_id": "exec_req_005"})

    # TESTFALL 6: Aufgabe mit fehlendem 'command_type' (sollte Fehler erzeugen)
    print("\n--- TESTFALL 6: Aufgabe mit fehlendem 'command_type' ---")
    payload_no_type = {"filename": "egal.txt", "details": "einige Details"} # command_type fehlt
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_no_type, {"original_request_id": "exec_req_006"})

    # TESTFALL 7: Aufgabe mit unbekanntem 'command_type' (sollte Fehler erzeugen)
    print("\n--- TESTFALL 7: Aufgabe mit unbekanntem 'command_type' ---")
    payload_unknown_type = {"command_type": "do_magic_trick", "details": "bitte schnell"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_unknown_type, {"original_request_id": "exec_req_007"})

    # TESTFALL 8: 'create_file' mit fehlendem 'filename' (sollte Fehler erzeugen)
    print("\n--- TESTFALL 8: 'create_file' mit fehlendem 'filename' ---")
    payload_create_no_filename = {"command_type": "create_file", "file_content": "dieser Inhalt hat keinen Dateinamen"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_create_no_filename, {"original_request_id": "exec_req_008"})

    # TESTFALL 9: 'read_file' mit fehlendem 'filename'
    print("\n--- TESTFALL 9: 'read_file' mit fehlendem 'filename' ---")
    payload_read_no_filename = {"command_type": "read_file"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_read_no_filename, {"original_request_id": "exec_req_009"})

    # TESTFALL 10: 'run_python_script' mit fehlendem 'script_code'
    print("\n--- TESTFALL 10: 'run_python_script' mit fehlendem 'script_code' ---")
    payload_python_no_code = {"command_type": "run_python_script"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_python_no_code, {"original_request_id": "exec_req_010"})

    # TESTFALL 11: 'execute_shell_command' mit fehlendem 'shell_command'
    print("\n--- TESTFALL 11: 'execute_shell_command' mit fehlendem 'shell_command' ---")
    payload_shell_no_command = {"command_type": "execute_shell_command"}
    dummy_planner.send_message(executor.agent_id, "execution_task", payload_shell_no_command, {"original_request_id": "exec_req_011"})

    print("\nLocalExecutionAgentInterface (command_types) Testläufe abgeschlossen.")
