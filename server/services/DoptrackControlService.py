from datetime import date, datetime, timedelta
from time import mktime
import rpyc
from rpyc.utils import classic
# import serial
import time
import re
import sys
import os
import yaml
import subprocess

from threading import Thread, Lock
from os import listdir
from os.path import isfile
#from gzip import GzipFile
import logging
from settings import BASE_DIR, LOC_AUTOMATION, LOC_PEN, LOC_ARM, LOC_REC, LOC_ZIP
from common import Files, ZipRecording

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True

logging.basicConfig(filename='/var/log/pythonDoptrackServer.log', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d CTRL %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


# This is the data structure used internal by the scripts on server saved as yml file.
# make_atq.sh uses this yml files to order the LOC_ARM list  
def getRecordingMetaData(NORADID, satelliteName, startOfRecording, sampleRate, lengthOfPass, tuningFrequency, webappuserid):
    data = {}
    data = {'Sat':{'State':{'Name': {}}, 'Predict':{}, 'Record':{}, 'Station':{}}}

    # input the State variables in the meta-structure
    data['Sat']['State']['Name'] = satelliteName
    data['Sat']['State']['NORADID'] = NORADID
    data['Sat']['State']['Tuning Frequency'] = tuningFrequency
    
    data['Sat']['State']['Antenna'] = 3 if 300000000 < tuningFrequency< 1000000000 else 1 
    data['Sat']['State']['Priority'] = 0       #  highest priority = 0, and its special for students using webapp

    # input the prediction variables into the meta-structure
    data['Sat']['Predict']['used TLE line1'] = ''
    data['Sat']['Predict']['used TLE line2'] = ''
    data['Sat']['Predict']['time used UTC'] = int(startOfRecording + '00')
    data['Sat']['Predict']['timezone used'] = ''
    data['Sat']['Predict']['Elevation'] = ''
    data['Sat']['Predict']['SAzimuth'] = ''
    data['Sat']['Predict']['EAzimuth'] = ''
    data['Sat']['Predict']['Length of pass'] = lengthOfPass

    # input the recording variables in the meta-structure
    data['Sat']['Record']['sample_rate'] = sampleRate
    data['Sat']['Record']['num_sample'] = sampleRate * lengthOfPass
    data['Sat']['Record']['time1 UTC'] = ''
    data['Sat']['Record']['time2 UTC'] = ''
    data['Sat']['Record']['time3 LT'] = ''
    data['Sat']['Record']['Start of recording'] = int(startOfRecording)
    data['Sat']['Record']['webappuserid'] = webappuserid

    # input for recording station (static info)
    data['Sat']['Station']['Name'] = 'DopTrack'
    data['Sat']['Station']['Lat'] = 51.01566305555556
    data['Sat']['Station']['Lon'] = 4.006821666666666
    data['Sat']['Station']['Height'] = 0.0
    return data

'''
# Deprecated
def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


# Deprecated
@singleton
class SafeZip:
    # Voorkomt dat meerdere recordingstegelijk ingezipt worden, of dat dit 2x gebeurd
    
    def __init__(self):
        self.lock = Lock()
    
    def zip(self, fileId):
        
        self.lock.acquire()
        try:            
            zipFilename = LOC_ZIP + fileId+ '.32fc.zip'
            if os.path.exists(zipFilename):
                return      # already zipped.
            
            command = 'zip ' + zipFilename + ' ' + LOC_REC + fileId+ '.*'
            logging.debug("shell executing command$ " + command)
            os.system(command)
            time.sleep(20)      # testing

        finally:
            self.lock.release()
'''

class DoptrackControlService(rpyc.Service):

    receiver = None
    def getReceiver(self):
        if self.receiver == None:
            self.receiver = rpyc.connect("localhost", 1234)
        return self.receiver.root

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_setFrequency(self, freq):
        return self.getReceiver().setFrequency(freq)

    def exposed_getFrequency(self):
        return self.getReceiver().getFrequency()

    def exposed_setAntenna(self, antenna):
        return self.getReceiver().setAntenna(antenna)

    def exposed_getAntenna(self):
        return self.getReceiver().getAntenna()

    # ______________________ test operations (deleted later)
    def exposed_test(self):
        return "OK"

    def exposed_testSleep(self, sec):
        time.sleep(sec)
        return "done sleeping"

    ################################
    # Call this function with care
    #   , for there can only be one process recording at a given time
    #   , and the scripts scedules recordings atomatic.  (find a way to detect if recorder is running or about to start [atq] )
    def exposed_recordDirect(self, callback, noradId, satelliteName, sampleRate, lengthOfRecording, tuningFrequency, webappuserid):
        
        startOfRecordingFormatted = datetime.now().strftime("%Y%m%d%H%M")
        filename = "_".join( (satelliteName, noradId, startOfRecordingFormatted ) )
        info = {'status': 'create metafile', 'filename': filename }
        callback(webappuserid, info)

        # ____ create record meta file
        data = getRecordingMetaData(noradId, satelliteName, startOfRecordingFormatted, sampleRate, lengthOfRecording, tuningFrequency, webappuserid)
        with open( LOC_REC + filename+'.yml', 'w') as outfile:
            outfile.write( yaml.dump(data, default_flow_style=False) )

        # ____ start recorder (if recorder is already running it abort uhd_rx_cfile command and return)
        info['status'] = 'created metafile, start recording'
        callback(webappuserid, info )
        numberOfSamples = sampleRate*lengthOfRecording
        start_rec_cmd = 'uhd_rx_cfile -a "addr=192.168.10.1" -f 45.07M --samp-rate=' + str(sampleRate) + ' -N ' + str(numberOfSamples) + ' ' + LOC_REC + filename + '.32fc'
        print start_rec_cmd
        recordingResult = os.system(start_rec_cmd)
        if recordingResult==0:
            info['status'] = 'finished recording, start compressing'
            callback(webappuserid, info)

            os.system('gzip -k -f -c ' + LOC_REC + filename + '.32fc > ' + LOC_REC + filename  + '.gz' )
         
            info['status'] = 'recording compressed'
            info['filenameCompressed'] = filename  + '.gz'
            callback(webappuserid, info)
        else:
            info['status'] = 'recording failed'
            callback(webappuserid, info)
            return "abort"
        return "done"

    # Maak en yml file in de PENDING directory en reschedule het geheel.
    def exposed_recordSchedule(self, noradId, satelliteName, sampleRate, lengthOfRecording, tuningFrequency, webappuserid, lStartOfRecording):
        startOfRecordingFormatted = datetime.fromtimestamp(lStartOfRecording).strftime("%Y%m%d%H%M")
        fileId = "_".join( (satelliteName, noradId, startOfRecordingFormatted ) )
        ymlFilename = LOC_PEN + fileId + '.yml'

        # ____ create record meta file
        data = getRecordingMetaData(noradId, satelliteName, startOfRecordingFormatted, sampleRate, lengthOfRecording, tuningFrequency, webappuserid)
        with open( ymlFilename, 'w') as outfile:
            outfile.write( yaml.dump(data, default_flow_style=False) )
            logging.info("added yml file: " + ymlFilename )
    
        return self.reorganizeArmedYmlFiles()

    # Verwijderyml file uit ARMED directory en reschedule het geheel.
    # Controle of gebruiker schedule mag verwijderen vind plaats in webapp want tijdslots leven daar
    def exposed_deleteSchedule(self, fileId):
        ymlFilename = LOC_ARM + fileId + '.yml'
        if os.path.exists(ymlFilename):
            try:
                os.remove(ymlFilename)
                return self.reorganizeArmedYmlFiles()
            except OSError, e:
                return "Error: %s - %s." % (e.filename,e.strerror)
        else:
            return "file %s not found." % filename


    # ######################## Berg-r
    # Mocht blijken dat make_atq.sh niet door 2 personen tegelijk aangeroepen kan worden dan moet deze geplaatst
    #  worden in de Singleton ReceiverService die dan hernoemd moet worden naar HardwareControl
    #############
    # Roep  make_atq.sh  om yml files in PENDING directory te mergen naar ARMED directory, en at joblist samen te stellen
    def reorganizeArmedYmlFiles(self):
        p = subprocess.Popen(LOC_AUTOMATION+'make_atq.sh', cwd=LOC_AUTOMATION, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        logging.info(LOC_AUTOMATION+"make_atq.sh\n" +
                     "____stdout: " + str(out) +
                     "____stderr: " + str(err) +
                     "____returncode: " + str(p.returncode))
        return "done" if p.returncode==0 else "error"

    '''
    # Dit werkt wel maar is extreem langzaam, NIET GEBRUIKEN DUS
    def exposed_zipRecording(self, name):
        import gzip
        import shutil
        zipname = "".join((LOC_REC, name, '.gz'))
        print "zipname: ", zipname, "   name: ", name
        with open(os.path.join(LOC_REC, name), 'rb') as f_in, gzip.open(zipname, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print "file zipped"
        return zipname
    '''

    # maak zip van recording en de yml. 
    def exposed_zipRecordingByOs(self, fileId):    
        zip = ZipRecording() 
        #zip = SafeZip()
        zip.zip(fileId)
        
        #command = 'zip ' + LOC_ZIP + fileId+ '.32fc.zip ' + LOC_REC + fileId+ '.*'
        #logging.debug("shell executing command$ " + command)
        #os.system(command)
        
    def exposed_getScheduleFileInfo(self):
        return Files().getScheduleFileInfo()


    def exposed_getRecordingFileInfo(self, filterDatesAfter):
        filterDatesAfter_local = classic.obtain(filterDatesAfter)
        return Files().getRecordingFileInfo(filterDatesAfter_local)

    def exposed_getImageFileInfo(self, noradid, filterDatesAfter, maxImages):
        filterDatesAfter_local = classic.obtain(filterDatesAfter)
        return Files().getImageFileInfo(noradid, filterDatesAfter_local, maxImages)
    

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    from rpyc.utils.authenticators import SSLAuthenticator
    port = 8080

    sslAuthenticator = SSLAuthenticator(keyfile=os.path.join(BASE_DIR, 'server.key'),
                                        certfile=os.path.join(BASE_DIR, 'server.crt'),
                                        ca_certs=os.path.join(BASE_DIR, 'client.crt')  )
    t = ThreadedServer(DoptrackControlService, port=port, authenticator=sslAuthenticator, protocol_config = rpyc.core.protocol.DEFAULT_CONFIG)
    
    logging.info( "Starting server (2 way SSL, self signed client/server cert) on port: " + str(port) )
    print "Starting server (2 way SSL, self signed client/server cert) on port: " + str(port)
    t.start()
