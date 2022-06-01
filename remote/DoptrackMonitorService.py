import datetime
import rpyc
import time
import sys
import os
import yaml
from threading import Thread
from os import listdir
from os.path import isfile, join
from settings import BASE_DIR, LOC_REC, LOC_ARM
import logging
from common import Files

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

logging.TRACE = 7	# DEBUG = 10			# monitor run (every 1 sec)
logging.SUPERTRACE = 3					# monitor event data send to client (can be every sec a lot of data)
logging.addLevelName(logging.TRACE, 'TRACE')			
logging.addLevelName(logging.SUPERTRACE, 'SUPERTRACE')

logging.basicConfig(filename='/var/log/DoptrackService.log', level=logging.TRACE, 
                    format='%(asctime)s.%(msecs)d MON %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
     

# Ik heb ze nu alle 3 in 1 exposed monitor class geplaatst, misschien is 3 apparte monitor classes beter  ?
class DoptrackMonitorService(rpyc.Service):

    #def exposed_test(self):
    #    x = datetime.now()
    #    logging.debug("Now " + str(x))
    #    return x

    # Op dit moment verzamelt elk status monitor object zijn eigen info, omdat er straks maar 1 client is is dit geen probleem.
    # anders moet er iets komen die al deze calls verzamelen en maar 1x uitvoeren.
    class exposed_StatusMonitor(object):
        def __init__(self, receiverEventCallback, scheduleEventCallback, recordingEventCallback, interval = 1):
            self.interval = interval
            self.prevReceiver = None
            self.prevSchedule = None
            self.prevRecording = None
            self.receiverEventCallback = rpyc.async(receiverEventCallback)   # create an async callback
            self.scheduleEventCallback= rpyc.async(scheduleEventCallback)    # create an async callback
            self.recordingEventCallback= rpyc.async(recordingEventCallback)  # create an async callback
            self.active = True
            self.thread = Thread(target = self.work)
            self.thread.start()
            logging.debug("StatusMonitor started: " + str(self))

        def exposed_stop(self):   # this method has to be exposed too
            self.active = False
            self.thread.join()    
            logging.debug("StatusMonitor stopped: " + str(self))


        def work(self):
            c = rpyc.connect("localhost", 1234)
            while self.active:
                logging.log( logging.TRACE, "StatusMonitor run: " + str(self))

                # ____ receiver
                currentReciever = {'frequency': c.root.getFrequency(),
                                   'antenna': c.root.getAntenna(), }
                if self.prevReceiver != currentReciever:
                    self.receiverEventCallback (currentReciever)
                    logging.log( logging.SUPERTRACE, "  receiverEvent to client: " + str(currentReciever))
                    self.prevReceiver = currentReciever

                # ____ Van alle geschedulde opnames (yml files in armed directory) de time, en length
                currentSchedule = Files().getScheduleFileInfo()
                if self.prevSchedule != currentSchedule:
                    self.scheduleEventCallback(currentSchedule)
                    logging.log( logging.SUPERTRACE, "  scheduleEvent to client: " + str(currentSchedule))
                    self.prevSchedule = currentSchedule
                                
                #____  Van alle opname en yml files van de afgeplopen 2 dagen
                filterDatesAfter = datetime.datetime.now() - datetime.timedelta(days=2)
                currentRecording = Files().getRecordingFileInfo(filterDatesAfter)
                if self.prevRecording != currentRecording:                    
                    self.recordingEventCallback(currentRecording )
                    logging.log( logging.SUPERTRACE, "  recordingEvent to client: " + str(currentRecording))
                    self.prevRecording = currentRecording

                time.sleep(self.interval)


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    from rpyc.utils.authenticators import SSLAuthenticator
    port = 8081

    sslAuthenticator = SSLAuthenticator(keyfile=os.path.join(BASE_DIR, 'server.key'),
                                        certfile=os.path.join(BASE_DIR, 'server.crt'),
                                        ca_certs=os.path.join(BASE_DIR, 'client.crt')  )
    t = ThreadedServer(DoptrackMonitorService, port=port, authenticator=sslAuthenticator, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)

    logging.info( "starting server (2 way SSL, self signed client/server cert) on port: " + str(port))
    t.start()
