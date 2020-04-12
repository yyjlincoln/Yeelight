from base import YeelightDevice, YeelightUnexcepted
from devicesdef import WifiBulb, WifiBulbConfig
import socket
import threading
from discover import Discover
import logger

class MusicServer():
    def __init__(self, host='0.0.0.0', port=54302):
        self.port = port
        self.host = host
        self.s = None

    def launch(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.host,self.port))
            self.s.listen(1)
            logger.log('Waiting for connection...')
            return True
        except:
            return False

    def next_device(self, originalDevice):    
        # Accept connection
        if not isinstance(originalDevice, YeelightDevice):
            raise YeelightUnexcepted('Not a yeelight device.')

        sx, addr = self.s.accept()
        print('Connection accepted.')
        o = WifiBulb(**originalDevice.__dict__)
        o.musicMode=True
        o.musicCtl=sx
        return o
    
    def terminate(self):
        try:
            self.s.close()
            return True
        except:
            return False