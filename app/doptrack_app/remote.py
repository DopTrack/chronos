'''
Created on 12 jul. 2016

Er zijn 2 server componenten 
- RemoteControl  (DEZE WORD GEBRUIKT  70 regels code) 
    - normale client server communicatie 
    - kan alles, taak schedulen, verwijderen , antenne zetten en gegevens opvragen.
    - Minder code en, eenvoudiger in gebruik
         
- RemoteServer   (MOMENTEEL NIET GEBRUIKT   200 regels code)
    - Experimenteel (client creert een monitor class op server en die informeert client als er iets veranderd)  
    - Geeft  alleen informate over   receiver, schedules en recordings
    - schedules en recordings zijn in exact hetzelfde formaat als RemoteControl.
    - geen netwerk verkeer als er geen verandering is   
    

@author: richardberg
'''
import rpyc
from rpyc.utils import classic
from rpyc.core.protocol import DEFAULT_CONFIG 

from threading import Thread, Lock
import os
import time
import sys
import re
from datetime import date, datetime, timedelta
from doptrack.settings import DOPTRACK_CLIENT_KEY, DOPTRACK_CLIENT_CRT, DOPTRACK_CA_CERTS, DOPTRACK_MON_PORT, DOPTRACK_CTRL_PORT, DOPTRACK_SERVER, DEBUG
from copy import copy, deepcopy
from django.core.cache import caches

# datetime word overgezet als weak reference
DEFAULT_CONFIG['allow_pickle'] = True

def on_receiverEvent(info):
    RemoteServer()._setReceiver(info)
    if DEBUG: print "MONITOR  receiverChanged: ", info


def on_scheduleEvent(info):
    RemoteServer()._setSchedule(info)
    if DEBUG: print "MONITOR  scheduleChanged: ", info


def on_recorderEvent(info):
    RemoteServer()._setRecord(info)
    if DEBUG: print "MONITOR  recorderChanged: ", info


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


# Deze class maakt een verbinding met doptrackserver waarna de server op eigen initiatief informatie doorstuurt naar deze client.
#   om preciezer te zijn als er een verandering heeft plaatsgevonden.
# Hoewel dit een mooie techniek is die goed werkt en netwerk verkeer verminderd gebruik ik het volgende keer niet meer.
#   iets lastiger debuggen en iets meer code.
#
# Beter had geweest: 
#   - Een singleton op de server waar de informatie staat en dat de clienten deze info krijgen op aanvraag.
#   - gedurende 2 sec oude info doorsturen, anders opnieuw bepalen.
#   - ook een singleton op deze webapp  opdat niet elke gebruiker resulteerd in netwerk verkeer met dezelfde info. (2 sec oude data hergebruiken)
@singleton
class RemoteServer():

    def __init__(self):
        self.cMon = None                # rpyc objects
        self.bgsrv = None
        self.mon = None

        self.lastDataReceived = 0       # last data received from server
        self.error = []
        self.serverStatus = ""
        self.schedule = None            # rpyc data    (when connection failes this object is gone)
        self.record = None
        self.receiver = None

        self.scheduleStale = []         # local copy of rpyc data
        self.recordStale = []
        self.receiverStale = []

        self.precConnectTime = 0        # last connection time

        self.lock = Lock()
        self.connectDoptrackServer()

    def test(self):
        xx = self.cMon.root.test()
        print xx     # maar jaar kun je niet opvragen want xx is weak reference
        yy = classic.obtain(xx)
        print yy.year

    # no guarenty this method is called
    def __del__(self):
        self.releaseDoptrackServer()
        time.sleep(1)
        if DEBUG: print "EXIT RemoteServer"

    # store rpyc raw data
    def _setReceiver(self, info):
        if DEBUG: print "new receiver data stored"
        self.lastDataReceived = time.time()
        self.receiver = info

    def _setSchedule(self, info):
        if DEBUG: print "new schedule data stored"
        self.lastDataReceived = time.time()
        self.schedule = info

    def _setRecord(self, info):
        if DEBUG: print "new recording data stored"
        self.lastDataReceived = time.time()
        self.record = info

    # When connection beaks down the raw rpyc data can not be read annymore.
    # So preprocess and copy  data, and also store it.
    # But keep processing the raw data to detect connection errors.
    def getReceiver(self):
        self.error = []
        try:
            data = {}
            data['frequency'] = self.receiver['frequency']
            data['antenna'] = self.receiver['antenna']
            self.receiverStale = data
        except:
            self.error.append("error during processing receiver data  (reconnect server monitor and for now return stale data)")
            self.connectDoptrackServer()
        return self.receiverStale

    def getSchedule(self):
        self.error = []
        try:
            self.scheduleStale = copy(self.schedule)
        except:
            e = sys.exc_info()[0]
            self.error.append("error during prosessing schedule data  (reconnect server monitor and for now return stale data)")
            self.connectDoptrackServer()
        return self.scheduleStale

    def getRecord(self):
        self.error = []
        try:
            self.recordStale = copy(self.record)
        except:
            e = sys.exc_info()[0]
            self.error.append("error during processing record data (reconnect server monitor and for now return stale data)")
            self.connectDoptrackServer()
        return self.recordStale

    # return feedback to user shown in webapp
    def getFeedbackList(self):
        _error = list(self.error)

        if(self.serverStatus):
            _error.append(self.serverStatus)

            # als er geen verbinding is dan pas laten zien wanneer laatste verbinding was
            if(self.lastDataReceived < (time.time()-1*60)):
                _error.append("Last information from server received on: " + str(time.ctime(int(self.lastDataReceived))))

        self.error = []
        # print _error
        return _error



    # The webapp user can call this method too, in case of problems an attempt to reconect to server.
    def connectDoptrackServer(self):

        self.lock.acquire()
        try:
            # prevent connection dockpile, resulting in invalid data objects and more reconnects
            maxConnectAttemptTimeInterval = 5
            if (self.precConnectTime + maxConnectAttemptTimeInterval) > time.time():
                if DEBUG: print "dont connect now, last attempt was less than "+str(maxConnectAttemptTimeInterval)+" sec ago"
                return
            self.precConnectTime = time.time()

            self.releaseDoptrackServer()
            self.serverStatus = "Not connected"

            if DEBUG: print "create connection ", str(self.precConnectTime)
            self.cMon = rpyc.ssl_connect(DOPTRACK_SERVER, DOPTRACK_MON_PORT,
                                         keyfile=DOPTRACK_CLIENT_KEY,
                                         certfile=DOPTRACK_CLIENT_CRT,
                                         ca_certs=DOPTRACK_CA_CERTS, config=DEFAULT_CONFIG)
            self.bgsrv = rpyc.BgServingThread(self.cMon)
            self.mon = self.cMon.root.StatusMonitor(on_receiverEvent, on_scheduleEvent, on_recorderEvent)
            self.serverStatus = None

        except:
            self.serverStatus = "failed to (re) connect to server: " + str(time.strftime("%H:%M:%S", time.localtime(time.time())))

        finally:
            self.lock.release()

    def releaseDoptrackServer(self):
        if DEBUG: print "release connection"
        try:
            if self.mon:
                self.mon.stop()
                self.mon = None
            if self.bgsrv:
                self.bgsrv.stop()
                self.bgsrv = None
            if self.cMon:
                self.cMon.close()
                self.cMon = None
            if DEBUG: print "release connection done"
        except:
            print "failed to release connection"


# Deze class communiceert met de doptrack server op de normale manier.
#   (call naar server en server antwoord.)
class RemoteControl():

    def __init__(self):
        self._c = None                # rpyc objects

    # no guarenty this method is called
    def __del__(self):
        self.releaseDoptrackServer()
        
    def getRoot(self):
        if not self._c:
            if DEBUG: print "create connection "
            try:
                self._c = rpyc.ssl_connect(DOPTRACK_SERVER, DOPTRACK_CTRL_PORT,
                                          keyfile=DOPTRACK_CLIENT_KEY,
                                          certfile=DOPTRACK_CLIENT_CRT,
                                          ca_certs=DOPTRACK_CA_CERTS, config=DEFAULT_CONFIG)
                if DEBUG: print "RemoteControl connection READY"
            except:
                e = sys.exc_info()[0]
                msg = "failed to connect to server: " + str(e)
                raise Exception(msg)
        return self._c.root  
    
    def releaseDoptrackServer(self):
        if self._c:
            if DEBUG: print "release connection"
            try:
                if self._c:
                    self._c.close()
                    self._c = None
                if DEBUG: print "release connection done"
            except:
                print "failed to release connection"
    

    def addRecordSchedule(self, noradid, satelitename, lengthSec, freq, userId, startTime):
        lSchedule = time.mktime(startTime.timetuple())
        return self.getRoot().recordSchedule(noradid, satelitename, 250000, lengthSec, freq, userId, lSchedule)

    def deleteSchedule(self, fileId):
        self.getRoot().deleteSchedule(fileId)

    # zippen van 1.5 GB gebruikt veel van OS op server en deze taak mag slechts 1x gestart worden,  
    def zipRecording(self, fileId):
        #cacheId = 'zip_' + fileId
        
        #zip = caches['default'].get(cacheId);
        #if not zip:
        createZipAsyn = rpyc.async(self.getRoot().zipRecordingByOs)
        resultAsynCall = createZipAsyn(fileId)
        #caches['default'].set('zip_' + fileId, 'OS on server is zipping this file, please wait for 3 min', 180);

    def getScheduleFileInfo(self):
        schedule = caches['default'].get('schedule');
        if not schedule:
            schedule = self.getRoot().getScheduleFileInfo()
            schedule = classic.obtain(schedule)                         # no netrefs, I just want values
            caches['default'].set('schedule', schedule, 5)
        return schedule

    def getRecordingFileInfo(self, dayFilter):
        cacheId = 'recordings_'+ str(dayFilter)
        secondsToCache = 5 if dayFilter<3 else 15                       # het kost 11 sec om alles op te halen 
        
        recording = caches['default'].get(cacheId)
        if not recording:
            filterDatesAfter = datetime.now() - timedelta(days=int(dayFilter))
            recording = self.getRoot().getRecordingFileInfo(filterDatesAfter)
            recording = classic.obtain(recording)                         # no netrefs, I just want values
            caches['default'].set(cacheId, recording, secondsToCache)
        return recording

    def getImageFileInfo(self, noradid, dayFilter, maxImages):
        cacheId = '_'.join( ('images', str(noradid), str(dayFilter), str(maxImages) ) )
        if DEBUG: print "imageCacheId: " + cacheId
        secondsToCache = 3600
        
        images = caches['default'].get(cacheId)
        if not images:
            
            filterDatesAfter = datetime.now() - timedelta(days=int(dayFilter)) if dayFilter else None
            
            images = self.getRoot().getImageFileInfo( noradid, filterDatesAfter, maxImages) 
            images = classic.obtain(images)                         # no netrefs, I just want values
            caches['default'].set(cacheId, images, secondsToCache)
        return images


# Deze main operatie is er slechts om de remote connectie te testen en gebruikt voor ontwikkeling.
if __name__ == "__main__":

    for i in range(1, 900):
        try:
            remote = RemoteServer()
            if i ==1:
                time.sleep(5)   # wacht even anders loopt log door elkaar (kan wel maar is lelijk)
                
            print "__ LAST RECEIVER: ", remote.getReceiver()
            print "__ LAST Schedule: ", remote.getSchedule()
            print "__ LAST Recording: ", remote.getRecord()
            print ""
        except:
            e = sys.exc_info()[0]
            print "________________________________ ERROR", e
        finally:
            time.sleep(1)

    print "___________________________________ END OF TEST: "
    # RemoteServer().releaseDoptrackServer()
