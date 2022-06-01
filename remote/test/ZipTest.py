'''
Created on Nov 28, 2017

Simulatie van Inzippen van bestanden op server
 
Aantal bestanden dat tegelijk mag worden ingeziped is configureerbaar.
Er owrd een werklijst bijgehouden met welke inziptaken nog volgen. 
In de werklijst kunnen geen dubbele taken komen.
Er is uit te lezen welke taken er nog gedaan worden en waar nu aan gewerkt word.

@author: richard
'''
from threading import Lock, BoundedSemaphore
import time
from random import randint



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
class ZipTest:
    max_concurrentZip = 2
  
    def __init__(self):
        self.listlock = Lock()
        self.semaphoreZip =  BoundedSemaphore(self.max_concurrentZip)
        self.worklist = []
        self.processinglist = []
        print '    clear worklist'
    
    def zip(self, zipId):
        
        # _____________ worklist (geen dubbel werk aannemen, en ook deze check moet onder lock)
        self.listlock.acquire()
        try:
            if zipId in self.worklist:
                print 'SKIP already in worklist: ' + zipId + '  ' + (' worklist [%s]' % ', '.join(map(str, self.worklist)))
                return
        
            print 'ADD to worklist: ' + zipId + '  ' + (' worklist [%s]' % ', '.join(map(str, self.worklist)))
            self.worklist.append(zipId)
        finally:
            self.listlock.release()
            
        
        # _____________ worklist item uitvoeren        
        self.semaphoreZip.acquire()
        try:            
            self.processinglist.append(zipId)

            print '__________ZIPPING: ' + zipId + '  ' + (' worklist [%s]' % ', '.join(map(str, self.worklist)))
            time.sleep( randint(3, 7) )
            
        finally:
            self.processinglist.remove(zipId)
            self.worklist.remove(zipId)
            self.semaphoreZip.release()
    
    def getZipWorlkList(self):
        return self.worklist
    
    def getCurrentZipJobs(self):
        return self.processinglist


#z= ZipTest()                # als je deze gebruikt heb je gen singleton nodig
def zip(zipId):
    z= ZipTest()             # als je singleton tegelijk aanroept can kun je ook probleem hebben 
    z.zip(zipId)
    


from multiprocessing import Pool
import threading


if __name__ == '__main__':
    
    fileIds = []
    fileIds.append('aaaa')
    fileIds.append('bbbb')
    fileIds.append('aaaa')
    fileIds.append('bbbb')
    fileIds.append('aaaa')
    fileIds.append('bbbb')
    # 12 sec
    fileIds.append('cccc')
    fileIds.append('dddd')
    fileIds.append('cccc')
    fileIds.append('dddd')
    fileIds.append('eeee')
    fileIds.append('cccc')
    fileIds.append('dddd')
    fileIds.append('cccc')
    fileIds.append('dddd')
    fileIds.append('aaaa')   # zipping aaaa again, server has no memory of past jobs so its a new job
    fileIds.append('bbbb')
    fileIds.append('cccc')
    fileIds.append('dddd')
    

    threads = []
    for i in range( len(fileIds)):
        
        if i ==6:
            time.sleep(12);  # wait 12 sec voor verwerken 1e cccc
            print '\nAfter break resume with : ' + fileIds[i]

        t = threading.Thread(target=zip, args=(fileIds[i],))         
        threads.append(t)
        t.start()
    print 'DONE'
    
    # Print nu alle jobs tot het klaar is 
    while len( ZipTest().getZipWorlkList() ) > 0:
        time.sleep(1)
        print '  Current zipJob: ' + str(ZipTest().getCurrentZipJobs());
    print 'ALLES IS KLAAR !'
    
'''        
# ______________________   pool werkt wel, maar omdat het een ander python processen zijn werkt lock niet meer.
    fileIds = []
    fileIds.append('aaaa')
    fileIds.append('bbbb')
    fileIds.append('aaaa')
    fileIds.append('bbbb')
    fileIds.append('aaaa')
    fileIds.append('cccc')
    fileIds.append('bbbb')
    fileIds.append('aaaa')
    fileIds.append('bbbb')
    
    pool = Pool(10)
    pool.map(zip, fileIds)
    pool.close() 
    pool.join()
    print 'DONE'
'''      

''' ______________________   geen goede test  omdat het 1 voor 1 gaat. 
    z = ZipTest()
    z.zip('aaaaa');
    z.zip('bbbb');
    z.zip('aaaaa');
    z.zip('cccc');
'''