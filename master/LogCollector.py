# LEVEL AÇIKLAMALARI İLE BERABER YAPIYOR

import win32evtlog
import json
import time

def get_security_event_logs():
    logs = []
    handle = win32evtlog.OpenEventLog(None, "Security")
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_records = win32evtlog.GetNumberOfEventLogRecords(handle)
    events = win32evtlog.ReadEventLog(handle, flags, 0)
    for event in events:
        # Level seviyesine göre belirli başlıklar ekle
        level_titles = {
            0: "Bilgi",
            1: "Denetim Basarisi",
            2: "Uyari",
            3: "Denetim Basarisizligi",
            4: "Hata",
            5: "Kritik",
            6: "Ozel",
            7: "Basarili Denetim",
            8: "Basarisiz Denetim"
        }
        log_data = {
            "EventID": event.EventID,
            "SourceName": event.SourceName,
            "Level": level_titles.get(event.EventType, "Bilinmeyen"),  # Level seviyesine karşılık gelen başlık
            # "Keywords": event.EventID,  # Keywords yerine EventID kullanıldı
            "Channel": "Security",
            "Message": event.StringInserts,
            # Diğer özellikler buraya eklenebilir
        }
        logs.append(log_data)
    win32evtlog.CloseEventLog(handle)
    return logs

def save_logs_to_json(logs, filename):
    with open(filename, "a") as f:
        for log in logs:
            json.dump(log, f)
            f.write("\n")
    print(f"Event logs appended to {filename}")

def main():
    while True:
        # Security event loglarını al
        security_logs = get_security_event_logs()

        # JSON formatına dönüştür ve dosyaya kaydet
        save_logs_to_json(security_logs, "Logs/OUTPUT.json")

        # 60 saniyede bir yenile
        time.sleep(60)

if __name__ == "__main__":
    main()
