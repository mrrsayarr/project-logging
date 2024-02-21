# GUI olmadan çalşıyor - Loglar sürekli olarak geliyor.
# JSON yok

import win32evtlog
import time

# Maksimum log sayısı
MAX_LOG_COUNT = 100

def get_all_event_logs():
    event_logs = []
    log_types = {
        "Application": "Application",
        "System": "System",
        "Security": "Security"
    }

    for log_name, log_type in log_types.items():
        handle = win32evtlog.OpenEventLog(None, log_name)
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
                if total_read >= total_records:
                    break

            if total_read >= total_records:
                break

        # Yeni loglar eklenirken eski loglar sınırı aşarsa, eski loglar silinir
        if len(events) > MAX_LOG_COUNT:
            events = events[-MAX_LOG_COUNT:]

        event_logs.append({
            "LogName": log_name,
            "LogType": log_type,
            "Events": events
        })

        win32evtlog.CloseEventLog(handle)

    return event_logs


def print_event_logs(event_logs):
    for log in event_logs:
        print(f"--- {log['LogName']} ---")
        for event in log["Events"]:
            print(f"Event ID: {event.EventID}, Time: {event.TimeGenerated}, Source: {event.SourceName}")

def main():
    while True:
        event_logs = get_all_event_logs()
        print_event_logs(event_logs)
        time.sleep(30)  # Yeniden kontrol etme aralığı (saniye cinsinden)

if __name__ == "__main__":
    main()
