# çalışıyor

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import win32evtlog
import json
import win32evtlogutil
# import subprocess # Yönetici ayrıcalıkları

# subprocess.call(["python", "1602.2210.py"], shell=True) # Yönetici ayrıcalıkları

# Maksimum log sayısı ve her log tipinden alınacak maksimum kayıt sayısı
MAX_TOTAL_LOGS = 10000
MAX_LOG_COUNT_PER_TYPE = 10000

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


def format_log_event(event):
    formatted_event = {
        "EventID": event.EventID,
        "TimeGenerated": event.TimeGenerated.Format(),
        "SourceName": event.SourceName,
        "Description": win32evtlogutil.SafeFormatMessage(event, 'Application')
    }
    return formatted_event


def write_logs_to_json(event_logs):
    data = {}
    for log in event_logs:
        log_name = log['LogName']
        log_type = log['LogType']
        data[log_name] = {
            "LogType": log_type,
            "Events": [format_log_event(event) for event in log['Events']]
        }

    with open("../event_logs.json", "w") as f:
        json.dump(data, f, indent=4)

processed_events = set()

def display_logs(event_logs):
    for log in event_logs:
        log_name = log['LogName']
        log_type = log['LogType']
        log_text = f"--- {log_name} ({log_type}) ---\n"
        for event in log['Events']:
            formatted_event = format_log_event(event)
            event_id = formatted_event['EventID']

            # EventID daha önce işlendiyse atla
            if event_id in processed_events:
                continue

            # EventID'yi işlenmiş olarak işaretle
            processed_events.add(event_id)

            # Log metnini oluştur
            log_text += f"Event ID: {event_id}, Time: {formatted_event['TimeGenerated']}, Source: {formatted_event['SourceName']}\n"
            #log_text += f"Description: {formatted_event['Description']}\n"
            log_text += "-" * 50 + "\n"  # Log satırı sonrası çizgi ekle
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
    write_logs_to_json(event_logs)
    root.after(3000, refresh_logs)  # SANİYE AYARLAMA
    # BURADA BAZEN SIKINTI ÇIKABİLİR


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
