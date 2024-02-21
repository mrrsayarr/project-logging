# Temel Veri çekme işlemlerini yapıyor
# JSON yok

import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import QTimer
import win32evtlog

class EventLogViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Event Log Viewer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.event_list_widget = QListWidget()
        layout.addWidget(self.event_list_widget)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.refresh_event_logs()
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_event_logs)
        self.timer.start(30000)  # 30 seconds interval for refreshing event logs

    def refresh_event_logs(self):
        event_logs = get_all_event_logs()
        self.event_list_widget.clear()
        self.label.setText("Last refreshed: " + time.strftime("%Y-%m-%d %H:%M:%S"))
        for log in event_logs:
            list_item = QListWidgetItem("--- " + log['LogName'] + " ---")
            self.event_list_widget.addItem(list_item)
            for event in log["Events"]:
                list_item = QListWidgetItem(f"Event ID: {event.EventID}, Time: {event.TimeGenerated}, Source: {event.SourceName}")
                self.event_list_widget.addItem(list_item)


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

        event_logs.append({
            "LogName": log_name,
            "LogType": log_type,
            "TotalRecords": total_records,
            "Events": []
        })

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total_read = 0
        while True:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if not events:
                break

            for event in events:
                event_logs[-1]["Events"].append(event)
                total_read += 1
                if total_read >= total_records:
                    break

            if total_read >= total_records:
                break

        win32evtlog.CloseEventLog(handle)

    return event_logs

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EventLogViewer()
    window.show()
    sys.exit(app.exec_())
