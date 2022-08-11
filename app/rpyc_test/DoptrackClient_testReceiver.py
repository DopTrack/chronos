import rpyc
import time
import sys
from datetime import date, datetime, timedelta
from gzip import GzipFile
import copy


from settings import (
    DOPTRACK_SERVER,
    DOPTRACK_CLIENT_KEY,
    DOPTRACK_CLIENT_CRT,
    DOPTRACK_CA_CERTS,
)

c = rpyc.ssl_connect(
    DOPTRACK_SERVER,
    8080,
    keyfile=DOPTRACK_CLIENT_KEY,
    certfile=DOPTRACK_CLIENT_CRT,
    ca_certs=DOPTRACK_CA_CERTS,
)


print c.root


# ________________________________________
orgFreq = c.root.getFrequency()
orgAntenna = c.root.getAntenna()

print "_____________ current"
print "Antenna: " + orgAntenna
print "Frequency: " + orgFreq


"""
print "_____________ change"
print "Antenna changed to: " + c.root.setAntenna(1)
print "Frequency changed to: " + c.root.setFrequency("0123456789")
time.sleep(1)
print "Antenna changed to: " + c.root.setAntenna(3)
print "Frequency changed to: " + c.root.setFrequency("0145870000")
time.sleep(1)

print "_____________ restore"
print "Antenna restored to: " + c.root.setAntenna(orgAntenna)
print "Frequency resored to: " + c.root.setFrequency(orgFreq)
"""


"""
# _____________ direct recording   (async met callback)
print "\n\n________ direct recording   (async met callback)"
def callback(userId, info):
    print "      callback: ", userId, info

recordRemote = rpyc.async(c.root.recordDirect)
recordAsy = recordRemote(callback, "32789", "Delfi-C5", 250000, 8, 145870000, 999999)
cnt = 0
while 1:
    time.sleep(1)

    cnt += 1
    print "Server is recording: " + str(cnt)
    if recordAsy.ready:
        print "Antwoord van server ", recordAsy.value
        break
"""

# ______________ kijken hoe snel je commandos aan receiver kunt geven en of dat dan conflicten geeft met meedere threads on server-
for i in range(1, 40):
    print "freq: ", c.root.getFrequency(), "  antenna: ", c.root.getAntenna()


print "__________________ STOP ALL"
c.close()
