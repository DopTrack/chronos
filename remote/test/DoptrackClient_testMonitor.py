import rpyc
import time
import sys
from datetime import date, datetime, timedelta
from gzip import GzipFile
import copy 

#  


c = rpyc.ssl_connect("doptrack.tudelft.nl", 8080, keyfile='../client.key', certfile ='../client.crt', ca_certs='../server.crt' )
print c.root

cMon = rpyc.ssl_connect("doptrack.tudelft.nl", 8081, keyfile='../client.key', certfile ='../client.crt', ca_certs='../server.crt' )
print cMon.root


print "\nStarting monitor, it should report data imediate"
bgsrv = rpyc.BgServingThread(cMon)

def on_receiverEvent(info):
    print "MONITOR  receiverChanged: ", info
def on_scheduleEvent(info):
    print "MONITOR  scheduleChanged: ", info
def on_recorderEvent(info):
    print "MONITOR  recorderChanged: ", info

mon = cMon.root.StatusMonitor(on_receiverEvent, on_scheduleEvent, on_recorderEvent)

time.sleep(2)
print "\nsleeping now for 10 seconds nothing should happen"
time.sleep(8)


print "\nInsert a new schedule, Monitor should report changes"
schedule = datetime.now() + timedelta(minutes=1)
lSchedule = time.mktime(schedule.timetuple())
result = c.root.recordSchedule("32789", "bergtest-C4", 250000, 8, 145870000, 999999, lSchedule)
c.close()
print "Result for scheduled recording: ", result



print "\n_________________ Monitor is still running, When recording starts it should report the changes."
time.sleep(120)


print "__________________ STOP MONITOR, end of test"

mon.stop()
bgsrv.stop()
cMon.close()