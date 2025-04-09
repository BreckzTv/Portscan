import socket
import concurrent.futures
import colorama
import whois

banner=r"""
 ,________________________________       
|__________,----------._ [____]  ""-,__  __...-----==="
        (_(||||||||||||)___________/   ""             |
           `----------'        [ ))"-,                |
                                ""    `,  _,--...___  |
                                        `/
       owner@github.com/breckztv          
"""

def get_ip_address(url):
    try:
        return socket.gethostbyname(url)
    except socket.gaierror:
        print("Konnte die URL nicht auflösen.")
        exit()

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex((ip, port)) == 0
    except Exception as e:
        print(f"Fehler beim Überprüfen des Ports {port}: {e}")
        return False

def scan_port(ip, port):
    if is_port_open(ip, port):
        try:
            service = socket.getservbyport(port, 'tcp')
        except OSError:
            service = "Unbekannter Dienst"
        return port, service
    return None

def scan_ports(ip, start_port, end_port):
    print("Scanning Ports....")
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)

    for port, service in open_ports:
        print("\033[31m"+ banner)
        print(f"Offener Port gefunden: {URL} {ip} {port} (tcp, {service})")
        input("Beliebige Taste drücken um zu beenden")
if __name__ == "__main__":
    URL = input("Geben Sie die URL ein: ")
    IP_ADRESSE = get_ip_address(URL)
    scan_ports(IP_ADRESSE, 1, 1024)  # Scan ports from 1 to 1024


