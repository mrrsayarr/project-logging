# Klasör oluşturup logları oraya topluyor

import os
import codecs
import sys
import time
import traceback
import win32con
import win32evtlog
import win32evtlogutil
import winerror

def getAllEvents(server, logtypes, basePath):
    if not server:
        serverName = "localhost"
    else:
        serverName = server
    for logtype in logtypes:
        path = os.path.join(basePath, "%s_%s_log.log" % (serverName, logtype))
        if not os.path.exists(basePath):
            os.makedirs(basePath)
        getEventLogs(server, logtype, path)

def getEventLogs(server, logtype, logPath):
    print("Logging %s events" % logtype)
    with codecs.open(logPath, encoding='utf-8', mode='w') as log:
        line_break = '-' * 80
        log.write("\n%s Log of %s Events\n" % (server, logtype))
        log.write("Created: %s\n\n" % time.ctime())
        log.write("\n" + line_break + "\n")
        hand = win32evtlog.OpenEventLog(server, logtype)
        total = win32evtlog.GetNumberOfEventLogRecords(hand)
        print("Total events in %s = %s" % (logtype, total))
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        evt_dict = {
            win32con.EVENTLOG_AUDIT_FAILURE: 'EVENTLOG_AUDIT_FAILURE',
            win32con.EVENTLOG_AUDIT_SUCCESS: 'EVENTLOG_AUDIT_SUCCESS',
            win32con.EVENTLOG_INFORMATION_TYPE: 'EVENTLOG_INFORMATION_TYPE',
            win32con.EVENTLOG_WARNING_TYPE: 'EVENTLOG_WARNING_TYPE',
            win32con.EVENTLOG_ERROR_TYPE: 'EVENTLOG_ERROR_TYPE'
        }
        try:
            while events:
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                for ev_obj in events:
                    the_time = ev_obj.TimeGenerated.Format()  # '12/23/99 15:54:09'
                    evt_id = str(winerror.HRESULT_CODE(ev_obj.EventID))
                    computer = str(ev_obj.ComputerName)
                    cat = ev_obj.EventCategory
                    record = ev_obj.RecordNumber
                    msg = win32evtlogutil.SafeFormatMessage(ev_obj, logtype)
                    source = str(ev_obj.SourceName)
                    if not ev_obj.EventType in evt_dict.keys():
                        evt_type = "unknown"
                    else:
                        evt_type = str(evt_dict[ev_obj.EventType])
                    log.write("Event Date/Time: %s\n" % the_time)
                    log.write("Event ID / Type: %s / %s\n" % (evt_id, evt_type))
                    log.write("Record #%s\n" % record)
                    log.write("Source: %s\n\n" % source)
                    log.write(msg)
                    log.write("\n\n")
                    log.write(line_break)
                    log.write("\n\n")
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
    print("Log creation finished. Location of log is %s" % logPath)


if __name__ == "__main__":
    server = None  # None = local machine
    logTypes = ["System", "Application", "Security"]
    basePath = r"C:\downloads"
    getAllEvents(server, logTypes, basePath)
