import admin
admin.run_as_admin()

import win32evtlog
from event_descriptions import get_event_descriptions  # Security Event ID açıklamalarını getiriyor
import time
import socket

hostname = socket.gethostname()
MAX_TOTAL_LOGS = 1000 # Maksimum log sayısı ve her log tipinden alınacak maksimum kayıt sayısı
MAX_LOG_COUNT_PER_TYPE = 1000

def get_event_logs(log_type):
    handle = win32evtlog.OpenEventLog(None, log_type)
    total_records = win32evtlog.GetNumberOfEventLogRecords(handle)

    events = []
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_read = 0
    seen_event_ids = set()  # Görülen Event ID'leri izlemek için bir küme oluştur
    while True:
        new_events = win32evtlog.ReadEventLog(handle, flags, 0)
        if not new_events:
            break

        for event in new_events:
            if event.EventID in seen_event_ids:
                continue  # Eğer Event ID zaten görülmüşse bir sonraki olaya geç
            else:
                events.append(event)
                seen_event_ids.add(event.EventID)  # Görülen Event ID'lerini kaydet
                total_read += 1
                if total_read >= total_records or len(events) >= MAX_LOG_COUNT_PER_TYPE:
                    break

        if total_read >= total_records or len(events) >= MAX_LOG_COUNT_PER_TYPE:
            break

    win32evtlog.CloseEventLog(handle)
    return events

def get_all_event_logs():
    event_logs = []
    log_types = {
        "Security": "Security"  # Sadece Security
    }

    for log_name, log_type in log_types.items():
        events = get_event_logs(log_type)[:MAX_LOG_COUNT_PER_TYPE]
        event_logs.append({
            "LogName": log_name,
            "LogType": log_type,
            "Events": events
        })

    return event_logs

def format_log_event(event):
    event_id = event.EventID  # Olay ID'sini al
    event_descriptions = get_event_descriptions()  # Açıklamaları almak için fonksiyonu çağır
    description = event_descriptions.get(event_id, "Açıklama bulunamadı / Not Found Description")  # Sözlükten açıklamayı al, yoksa varsayılan bir değer dön
    return (f"Event ID: {event_id}, "
            f"Time: {event.TimeGenerated}, "
            f"Source: {event.SourceName}, "
            f"Description: {description}"
            )

def display_logs(event_logs):
    for log in event_logs:
        log_name = log['LogName']
        log_type = log['LogType']
        # print(f"--- {log_name} ({log_type}) ---") # Log Tipini başlık olarak yazdırur

        for event in log['Events']:
            log_text = format_log_event(event)
            print(log_text)
            # print("-" * 1)  # Log satırı sonrası çizgi ekle

def refresh_logs():
    while True:
        event_logs = get_all_event_logs()
        display_logs(event_logs)
        time.sleep(30)

refresh_logs() # Logları güncelle
