from base import YeelightDevice, YeelightUnexcepted
from devicesdef import WifiBulb, WifiBulbConfig
import socket
import threading
from discover import Discover

s = None

def launchServer(port=54302):
    global s
    # Get the server ready to go
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',port))
    s.listen(1)
    print('Waiting for connection...')

def nextDevice(device):    
    # Accept connection
    if not isinstance(device, YeelightDevice):
        raise YeelightUnexcepted('Not a yeelight device.')

    sx, addr = s.accept()
    print('Connection accepted.')
    s.close()
    o = WifiBulb(**device.__dict__)
    o.musicMode=True
    o.musicCtl=sx
    return o
    

launchServer(8080)
ds = Discover(WifiBulbConfig)
dev = ds.discover()

for x in dev:
    mainctl = dev[x]

mainctl.set_power('on')
mainctl.set_music(1, '192.168.20.4',8080)
x = nextDevice(mainctl)
import random
import time
while True:
    print('inloop')
    x.set_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255), smooth = False, duration = 50)

x.set_power('off')
