import os
import sys
from threading import Thread, Lock
import serial
import re
import rpyc
from rpyc.utils.authenticators import AuthenticationError


import logging
logging.TRACE = 7	# DEBUG = 10
logging.basicConfig(filename='/var/log/DoptrackService.log', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d REC %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class ReceiverControl:

    def __init__(self):
        logging.info( "Created Receiver control (singleton)" )
        self.lock = Lock()

    # The singleton and lock make sure only one is allowed to comunicate with with receiver hardware, the rest must wait
    def send(self, command, loglevel=logging.TRACE):
        self.lock.acquire()
        try:
            ser = serial.Serial(port='/dev/ttyUSB0',
                                baudrate=115200,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=1)
            ser.write(command)
            out = ser.readline()
            logging.log( loglevel, ">> " + command.rstrip('\n\r')+ "  result: " + out.rstrip('\r\n') )
            ser.close()
            return out
        finally:
            self.lock.release()

    def setFrequency(self, freq):
        freq10Digit = "%010d" % (int(freq),)
        self.send('CF'+freq10Digit + '\r\n', logging.INFO)
        return self.getFrequency()

    def getFrequency(self):
        out = self.send('CF\r\n')
        try:
            return re.search(r'\d+', out).group()
        except:
            logging.error("Failed to extract frequencey from: " + str(out))

    def setAntenna(self, antenna):
        antennaNr = int(antenna)
        if not(antennaNr in (1, 2, 3)):
            raise "Only antenna 1, 2 or 3 is allowed"

        self.send('AN'+str(antenna)+'\r\n', logging.INFO)
        return self.getAntenna()

    def getAntenna(self):
        out = self.send('AN\r\n')
        try:
            return re.search(r'\d', out).group()
        except:
            logging.error("Failed to extract antenna from: " + str(out))

    # extra function that could replace all 4 operations above
    #   (dont use it, its better to hide hardware specific settings from remote client.)
    def sendToReceiver(self, command):
        return self.send(command)


class ReceiverService(rpyc.Service):

    receiver = ReceiverControl()

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_setFrequency(self, freq):
        return self.receiver.setFrequency(freq)

    def exposed_getFrequency(self):
        return self.receiver.getFrequency()

    def exposed_setAntenna(self, antenna):
        return self.receiver.setAntenna(antenna)

    def exposed_getAntenna(self):
        return self.receiver.getAntenna()


def only_local_authenticator(sock):
    peername = sock.getpeername()
    if not(peername[0] == '127.0.0.1'):
        logging.info( "access denied for: " + str(peername))
        raise AuthenticationError("only for internal use")
    return sock, None


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    port = 1234

    t = ThreadedServer(ReceiverService, port=port, authenticator=only_local_authenticator)

    logging.info( "starting ReceiverService (just for internal use) on port: " + str(port) )
    t.start()
