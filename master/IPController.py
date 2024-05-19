"""
DB Bağlasnıtısı oluşturuldu başarlı bir şekilde veriler yükleniyor

Output:
PID: 3288, Process: Spotify.exe, Local: 10.57.1.27:59321, Remote: 35.186.224.34:443, Protocol: ICMP (UDP)
PID: 23768, Process: chrome.exe, Local: 10.57.1.27:61259, Remote: 172.217.169.170:443, Protocol: ICMP (UDP)
PID: 23768, Process: chrome.exe, Local: 10.57.1.27:61281, Remote: 35.241.7.193:443, Protocol: ICMP (UDP)

Giden Gelen IP'ler kontrol edilir
Her 60 Saniyede Bir Bağlantıları Listeler
"""
import psutil
import time
import socket
import sqlite3

PROTOCOL_NAMES = {
    socket.IPPROTO_TCP: "TCP",
    socket.IPPROTO_UDP: "UDP",
    socket.IPPROTO_ICMP: "ICMP",
    # diğer protokoller
}

DB_PATH = 'Database.db'

def get_connections():
    connections = []
    for conn in psutil.net_connections():
        if conn.status == psutil.CONN_ESTABLISHED:
            local_addr = conn.laddr
            remote_addr = conn.raddr
            try:
                process_name = psutil.Process(conn.pid).name()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                process_name = "?"
            connection_key = f"{local_addr.ip}:{local_addr.port}-{remote_addr.ip}:{remote_addr.port}"
            connections.append({
                "pid": conn.pid,
                "local_address": f"{local_addr.ip}:{local_addr.port}",
                "remote_address": f"{remote_addr.ip}:{remote_addr.port}",
                "protocol": conn.type,
                "process_name": process_name,
                "key": connection_key
            })
    return connections

def send_alert(conn):
    # Uyarı gönderme mantığınızı buraya ekleyin
    # Örnek: E-posta, SMS veya log dosyasına yazma
    print(f"UYARI! Şüpheli bağlantı: {conn}")

def get_protocol_name(protocol_num):
    return PROTOCOL_NAMES.get(protocol_num, "UNKNOWN")

def insert_connection_to_db(conn):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO IpLogs (PID, Process, Local, Remote, Protocol)
        VALUES (?, ?, ?, ?, ?)
    ''', (conn['pid'], conn['process_name'], conn['local_address'], conn['remote_address'], get_protocol_name(conn['protocol'])))
    db.commit()
    db.close()

if __name__ == "__main__":
    seen_connections = set()
    while True:
        connections = get_connections()
        for conn in connections:
            if conn['key'] not in seen_connections:
                seen_connections.add(conn['key'])
                # Şüpheli bağlantıları kontrol edin (örnek kural)
                if conn['remote_address'].startswith("10.57.1.27"):  # Şüpheli IP aralığı
                    send_alert(conn)
                else:
                    insert_connection_to_db(conn)
                    protocol_name = get_protocol_name(conn['protocol'])
                    protocol_type = "TCP" if conn['protocol'] == socket.IPPROTO_TCP else "UDP"
                    print(f"PID: {conn['pid']}, Process: {conn['process_name']}, "
                          f"Local: {conn['local_address']}, Remote: {conn['remote_address']}, "
                          f"Protocol: {protocol_name} ({protocol_type})")
        time.sleep(60)
