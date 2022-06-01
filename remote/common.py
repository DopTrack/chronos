from datetime import date, datetime, timedelta
from time import mktime
import time
import yaml
import re
import sys
import os
from os import listdir
from os.path import isfile
import logging
from PIL import Image

from threading import Lock, BoundedSemaphore

from settings import BASE_DIR, LOC_AUTOMATION, LOC_PEN, LOC_ARM, LOC_REC, LOC_ZIP, LOC_IMAGE, LOC_THUMB



def singleton(class_):
    instances = {}
    instancelock = Lock()

    def getinstance(*args, **kwargs):
        try:
            instancelock.acquire()      # ook hier met lock afdwingen dat volgende controle niet plaatsvind voordat initieel object is toegevoegd.
            if class_ not in instances:
                instances[class_] = class_(*args, **kwargs)
            return instances[class_]
        finally:
            instancelock.release()
    return getinstance

@singleton
class ZipRecording:
    max_concurrentZip = 1
  
    def __init__(self):
        self.listlock = Lock()
        self.semaphoreZip =  BoundedSemaphore(self.max_concurrentZip)
        self.worklist = []
        self.processinglist = []
    
    def zip(self, zipId):        
        zipFilename = LOC_ZIP + zipId+ '.32fc.zip'
        logging.info("Zip " + zipFilename )

        # _____________ worklist bijhouden
        self.listlock.acquire()
        try:
            if zipId in self.worklist:
                return      # already in worklist

            if os.path.exists(zipFilename):
                return      # already zipped.
        
            self.worklist.append(zipId)
        finally:
            self.listlock.release()
        
        # _____________ ziptaak uitvoeren        
        self.semaphoreZip.acquire()
        try:            
            self.processinglist.append(zipId)

            # zip
            command = 'zip ' + zipFilename + ' ' + LOC_REC + zipId+ '.*'
            logging.debug("shell executing command$ " + command)
            os.system(command)
            
        finally:
            self.processinglist.remove(zipId)
            self.worklist.remove(zipId)
            self.semaphoreZip.release()
            
    
    def getZipWorlkList(self):
        return self.worklist
    
    def getCurrentZipJobs(self):
        return self.processinglist


# sort function
REGEX_DATE = re.compile(".*_\d+_(\d+).*$")
def dateNumberSort(value):
    m = REGEX_DATE.search(value)
    return m.group(1) if m else value


class Files(object):

    def getScheduleFileInfo(self):
        dataList = []

        fileIds = [f.replace(".yml", "") for f in listdir(LOC_ARM) if isfile(os.path.join(LOC_ARM, f)) and f.endswith('.yml')]
        for id_ in fileIds:

            data = {'id': id_}
            try:
                m = re.match(".*_(\d+)$", id_)
                if m:
                    fileNameTime = time.strptime(m.group(1), "%Y%m%d%H%M")              # yyyymmddhhmm
                    data['time'] = datetime.fromtimestamp(mktime(fileNameTime))
                else:
                    continue            # wrong yml file format

                ymmlFileName = os.path.join(LOC_ARM, id_ + '.yml')
                try:
                    with open(ymmlFileName, 'r') as metaf:
                        meta = yaml.load(metaf)
                        data['length'] = meta['Sat']['Predict']['Length of pass']
                        if 'webappuserid' in meta['Sat']['Record']:
                            data['userid'] = meta['Sat']['Record']['webappuserid']
                except:
                    logging.info("FAILED to process file: " + str(sys.exc_info()[0]) + "  " + ymmlFileName)
            except:
                logging.info("FAILED to process file: " + str(sys.exc_info()[0]) + "  " + id_)

            dataList.append(data)

        dataList = sorted(dataList, key=lambda x: x['time'], reverse=True)
        return dataList


    # 1 month of recordings takes 1 sec all takes 11 sec 
    def getRecordingFileInfo(self, filterDatesAfter):
        recordDataList = []
        zip = ZipRecording()
        
        recordFileIds = [f.replace(".yml", "") for f in listdir(LOC_REC) if isfile(os.path.join(LOC_REC, f)) and f.endswith('.yml')]
        for id in recordFileIds:

            recordData = {}
            try:
                ymmlFileName = os.path.join(LOC_REC, id + '.yml')
                recFileName = os.path.join(LOC_REC, id + '.32fc')
                zipFileName = os.path.join(LOC_ZIP, id + '.32fc.zip')

                # os operaties kosten veel tijd dus eerst maar eens datumtijd uit filenaam halen.
                m = re.match(".*_(\d+)$", id)
                if m:
                    fileNameTime = time.strptime(m.group(1), "%Y%m%d%H%M")              # yyyymmddhhmm
                    fileNameDate = datetime.fromtimestamp(mktime(fileNameTime))
                    recordData['time'] = fileNameDate
                else:
                    continue            # wrong yml file format

                if (filterDatesAfter and filterDatesAfter > fileNameDate):
                    continue            # Dit bestand is te oud

                recordData['id'] = id

                # get recording length (HEAVY OPERATION: reading all yml files takes 9 sec)
                try:
                    with open(ymmlFileName, 'r') as metaf:
                        meta = yaml.load(metaf)
                        recordData['length'] = meta['Sat']['Predict']['Length of pass']
                        if 'webappuserid' in meta['Sat']['Record']:
                            recordData['userid'] = meta['Sat']['Record']['webappuserid']
                except:
                    logging.info("FAILED to process file: " + str(sys.exc_info()[0]) + "  " + ymmlFileName)

                try: 
                    # recordData['time'] = datetime.fromtimestamp(os.path.getctime(recFileName))    # yml starttime is beter
                    recordData['recSize'] = os.path.getsize(recFileName)
                except:
                    pass    # file hoeft er niet te zijn

                # zip info
                try:
                    recordData['zipSize'] = os.path.getsize(zipFileName)
                except:
                    if id in zip.getZipWorlkList():
                        recordData['zipState'] = 'server busy'
                    if id in zip.getCurrentZipJobs():
                        recordData['zipState'] = 'zipping'                                            
                    
                # image info
                recordData['image'] = 'false'
                try:
                    if isfile(os.path.join(LOC_IMAGE, id+'_zoomedin.png')):
                        recordData['image'] = 'true'
                except:
                    recordData['image'] = 'error'

            except:
                logging.info("FAILED to process recording: " + str(sys.exc_info()[0]) + "  " + id )

            recordDataList.append(recordData)

        recordDataListSorted = sorted( recordDataList, key=lambda x: x['time'], reverse=True)
        return recordDataListSorted
    

    def getImageFileInfo(self, noradid, filterDatesAfter, maxImages ):

        imageFileNames = [f for f in listdir(LOC_IMAGE) if isfile(os.path.join(LOC_IMAGE, f)) and f.endswith('_zoomedin.png')]
        imageFileNames.sort(key=dateNumberSort, reverse=True)
        
        thumbFileNames = [f for f in listdir(LOC_THUMB) if isfile(os.path.join(LOC_THUMB, f)) and f.endswith('_thumb.png')]
        
        imageDataList = []
        for imageFilename in imageFileNames:
            
            # Filter op maximaal aantal images (Lijst is al gesorteerd op datum, dus je krijgt de nieuwste)
            if (maxImages and len(imageDataList)>=maxImages ):
               continue
            
            id = imageFilename.replace('_zoomedin.png','')
            
            imageData = {}
            imageData['id'] = id
            imageData['imageName'] = imageFilename
            imageData['thumbName'] = id + '_thumb.png'

            try:
                # os operaties kosten veel tijd dus eerst maar eens datumtijd uit filenaam halen.
                m = re.match("(.*)_(\d+)_(\d+)$", id)
                if m:
                    imageData['noradid'] = m.group(2)
                    
                    fileNameTime = time.strptime(m.group(3), "%Y%m%d%H%M")              # yyyymmddhhmm
                    fileNameDate = datetime.fromtimestamp(mktime(fileNameTime))
                    imageData['time'] = fileNameDate
                else:
                    continue            
                
                # filter op noradid
                if ( noradid and imageData['noradid']!=noradid ):
                    continue            
                
                # Filter om datum 
                if (filterDatesAfter and filterDatesAfter > fileNameDate):
                    continue
                
                # get recording length (HEAVY OPERATION: reading all yml files takes 9 sec)
                try:
                    ymmlFileName = os.path.join(LOC_REC, id + '.yml')
                    with open(ymmlFileName, 'r') as metaf:
                        meta = yaml.load(metaf)
                        imageData['length'] = meta['Sat']['Predict']['Length of pass']
                        if 'webappuserid' in meta['Sat']['Record']:
                            imageData['userid'] = meta['Sat']['Record']['webappuserid']
                except:
                    logging.info("FAILED to process file: " + str(sys.exc_info()[0]) + "  " + ymmlFileName)
                
                
                # create thumbnail if it does not exist
                try:
                    if not imageData['thumbName'] in thumbFileNames:
                        
                        # schrink to width 400 and keep same ratio
                        imagePathFileName = os.path.join(LOC_IMAGE, imageData['imageName'])
                        basewidth = 400
                        img = Image.open(imagePathFileName)
                        wpercent = (basewidth / float(img.size[0]))
                        hsize = int((float(img.size[1]) * float(wpercent)))
                        img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                        img.save( os.path.join(LOC_THUMB, imageData['thumbName']) )
                except:
                    logging.info("failed to create thumb image: " + str(sys.exc_info()[0]) + "  " + imageData['thumbName'])

            except:
                logging.info("FAILED to process image: " + str(sys.exc_info()[0]) + "  " + id )

            imageDataList.append(imageData)

        return imageDataList
