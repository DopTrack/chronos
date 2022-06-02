import rpyc
from rpyc.utils import classic
from rpyc.core.protocol import DEFAULT_CONFIG
import datetime

# datetime word anders overgezet als weak reference
DEFAULT_CONFIG['allow_pickle'] = True

c = rpyc.ssl_connect("doptrack.tudelft.nl", 8080, keyfile='../client.key', certfile ='../client.crt', ca_certs='../server.crt', config=DEFAULT_CONFIG )


    
print '__________________ scheduled informatie ophalen:'
result = c.root.getScheduleFileInfo()
result = classic.obtain(result)                              # no weak references, real data      

for recordInfo in result:
    print recordInfo



print '__________________ record informatie ophalen:'
filterDatesAfter = datetime.datetime.now() - datetime.timedelta(days=3)

result = c.root.getRecordingFileInfo(filterDatesAfter)
result = classic.obtain(result)                            # no weak references, real data

for recordInfo in result:
    print recordInfo



print '__________________ image informatie ophalen:'

filterDatesAfter = datetime.datetime.now() - datetime.timedelta(days=15)

result = c.root.getImageFileInfo('32789', filterDatesAfter)
result = classic.obtain(result)                           # no weak references, real data

for x in result:
    print x
 
    

c.close()



