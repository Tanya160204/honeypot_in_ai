import socket
import csv
import threading
from datetime import datetime
from termcolor import cprint

ASCII_ART = r"""

_________     _____   ____ ___  ________  ___ ______________ _____.___.________   ____ ___ 
\_   ___ \   /  _  \ |    |   \/  _____/ /   |   \__    ___/ \__  |   |\_____  \ |    |   \
/    \  \/  /  /_\  \|    |   /   \  ___/    ~    \|    |     /   |   | /   |   \|    |   /
\     \____/    |    \    |  /\    \_\  \    Y    /|    |     \____   |/    |    \    |  / 
 \______  /\____|__  /______/  \______  /\___|_  / |____|     / ______|\_______  /______/  
        \/         \/                 \/       \/             \/               \/          

"""

CSV_FILE = "intrusion_log.csv"

def log_to_csv(ip, port):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ip, port])

def handle_client(client_socket, addr, server_port):
    ip, _ = addr
    log_to_csv(ip, server_port)
    cprint(f"[!] Intrusion attempted from IP: {ip}, Port: {server_port}", "red", attrs=["bold"])

    response = f"""\
HTTP/1.1 200 OK\r
Content-Type: text/html\r
\r
<html>
  <body style="background-color:black; color:red; font-family:monospace; white-space: pre;">
    {ASCII_ART}
  </body>
</html>
"""
    try:
        client_socket.sendall(response.encode())
    except:
        pass
    client_socket.close()

def start_socket_on_port(port):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', port))
        server.listen(5)
        cprint(f"[*] Listening on port {port}", "red")

        while True:
            client_socket, addr = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, port))
            client_thread.start()

    except:
        pass

def main():
    cprint("[*] Starting Honeypot Server...", "red", attrs=["bold"])
    try:
        with open(CSV_FILE, 'r') as f:
            pass
    except FileNotFoundError:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "IP Address", "Port"])  # ✅ CORRECTED header

    for port in range(1, 1025):
        thread = threading.Thread(target=start_socket_on_port, args=(port,))
        thread.daemon = True
        thread.start()

    cprint("[*] Honeypot is live on ports 1-1024", "red", attrs=["bold"])
    while True:
        pass

if __name__ == "__main__":
    main()
