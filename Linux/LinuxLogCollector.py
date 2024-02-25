import os
import time
from datetime import datetime

def sort_logs_by_time(logs):
    # Her bir log satırını (tarih, saat, geri kalan) şeklinde bölme
    parsed_logs = [(datetime.strptime(log[:15], "%b %d %H:%M:%S"), log) for log in logs]
    # Tarih ve saat bilgisine göre sıralayalım
    sorted_logs = [log[1] for log in sorted(parsed_logs)]
    return sorted_logs

def read_log_file(log_file_path):
    logs = []
    try:
        with open(log_file_path, "r") as file:
            logs = file.readlines()
    except FileNotFoundError:
        print(f"{log_file_path} dosyası bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    return logs

def write_logs_to_file(logs, output_file):
    unique_logs = set()
    for log in logs:
        if log not in unique_logs:
            unique_logs.add(log)

    try:
        with open(output_file, "w") as file:
            for log in unique_logs:
                file.write(log.strip() + "\n")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

def main():
    log_collector_path = "/home/ros/Desktop/LogCollector/Log" # Log Path
    if not os.path.exists(log_collector_path):
        os.makedirs(log_collector_path)

    while True:
        apache_log_path = "/var/log/apache2/access.log" # Apache log dosyasının varlığını kontrol eder
        if os.path.exists(apache_log_path): # Apache log dosyası varsa, oku ve işle
            apache_logs = read_log_file(apache_log_path)
            apache_output_file = os.path.join(log_collector_path, "apache_access_logs.txt")
            sorted_apache_logs = sort_logs_by_time(apache_logs)
            write_logs_to_file(sorted_apache_logs, apache_output_file)

        auth_log_path = "/var/log/auth.log" # Auth log dosyasının varlığını kontrol eder
        if os.path.exists(auth_log_path): # Auth log dosyası varsa, oku ve işle
            auth_logs = read_log_file(auth_log_path)
            auth_output_file = os.path.join(log_collector_path, "auth_logs.txt")
            sorted_auth_logs = sort_logs_by_time(auth_logs)
            write_logs_to_file(sorted_auth_logs, auth_output_file)

        secure_log_path = "/var/log/secure" # Secure log dosyasının varlığını kontrol eder
        if os.path.exists(secure_log_path): # Secure log dosyası varsa, oku ve işle
            secure_logs = read_log_file(secure_log_path)
            secure_output_file = os.path.join(log_collector_path, "secure_logs.txt")
            sorted_secure_logs = sort_logs_by_time(secure_logs)
            write_logs_to_file(sorted_secure_logs, secure_output_file)

        # Her 30 saniyede bir döngüyü tekrarla
        time.sleep(30)

if __name__ == "__main__":
    main()

