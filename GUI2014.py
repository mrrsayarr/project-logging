# JSON VAR !!!
# KOD çalışıyor

# Sadece Security, Descrption kapalı

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import win32evtlog

from event_descriptions import get_event_descriptions # Security Event ID açıklamalarını getiriyor

# Maksimum log sayısı ve her log tipinden alınacak maksimum kayıt sayısı
MAX_TOTAL_LOGS = 1000
MAX_LOG_COUNT_PER_TYPE = 1000

def get_event_logs(log_type):
    handle = win32evtlog.OpenEventLog(None, log_type)
    total_records = win32evtlog.GetNumberOfEventLogRecords(handle)

    events = []
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_read = 0
    while True:
        new_events = win32evtlog.ReadEventLog(handle, flags, 0)
        if not new_events:
            break

        for event in new_events:
            events.append(event)
            total_read += 1
            if total_read >= total_records or len(events) >= MAX_LOG_COUNT_PER_TYPE:
                break

        if total_read >= total_records or len(events) >= MAX_LOG_COUNT_PER_TYPE:
            break

    win32evtlog.CloseEventLog(handle)
    return events

"""
# Log tiplerinden APP ve SYSTEM verilerini de getiriyor gereksiz

def get_all_event_logs():
    event_logs = []
    log_types = {
        "Application": "Application",
        "System": "System",
        "Security": "Security"
    }

    for log_name, log_type in log_types.items():
        events = get_event_logs(log_type)[:MAX_LOG_COUNT_PER_TYPE]
        event_logs.append({
            "LogName": log_name,
            "LogType": log_type,
            "Events": events
        })

    return event_logs
"""


def get_all_event_logs():
    event_logs = []
    log_types = {
        "Security": "Security" # Sadece Security
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
    description = event_descriptions.get(event_id, "Açıklama bulunamadı")  # Sözlükten açıklamayı al, yoksa varsayılan bir değer dön
    return (f"Event ID: {event_id}, "
            f"Time: {event.TimeGenerated}, "
            f"Source: {event.SourceName},\n "
            f"Description: {description}"
            )


def display_logs(event_logs):
    displayed_ids = set()  # Görüntülenen olay ID'lerini izlemek için bir küme oluştur

    for log in event_logs:
        log_name = log['LogName']
        log_type = log['LogType']
        log_text = f"--- {log_name} ({log_type}) ---\n"

        # Olayların ID'lerini kontrol et
        for event in log['Events']:
            if event.EventID in displayed_ids:
                continue  # Eğer olay ID'si zaten görüntülenmişse, bir sonrakine geç
            else:
                displayed_ids.add(event.EventID)  # Yeni bir olay ID'si ekleyin
                log_text += format_log_event(event) + "\n"
                log_text += "-" * 10 + "\n"  # Log satırı sonrası çizgi ekle

        log_text += "\n"

        if log_name == "Security":
            logs_text.insert(tk.END, log_text, "red_text")  # Kırmızı renkte vurgula
        else:
            logs_text.insert(tk.END, log_text)


def refresh_logs():
    logs_text.config(state=tk.NORMAL)
    logs_text.delete(1.0, tk.END)
    event_logs = get_all_event_logs()
    display_logs(event_logs)
    logs_text.config(state=tk.DISABLED)
    root.after(1000, refresh_logs)  # 1 saniyede refresh

root = tk.Tk()
root.title("Event Log Viewer")

# Scrollable text area for displaying logs
logs_text = ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
logs_text.pack(expand=True, fill=tk.BOTH)

# Create a custom tag for red text
logs_text.tag_configure("red_text", foreground="red")

# Start displaying logs
refresh_logs()

root.mainloop()
