from devicesdef import WifiBulbConfig
from discover import Discover

a = Discover(WifiBulbConfig)

a.discover()
print(a.discovered)
import time

for x in a.discovered:
    print(x, a.discovered[x].Location)
    sx = a.discovered[x]._connectToDevice()
    for d in range(5):
        res, sx = a.discovered[x].sendCommand(1,'set_bright',[1,'smooth',500], autoDisconnect = False, useExistingSocket = sx)
        time.sleep(0.5)
        res, sx = a.discovered[x].sendCommand(1,'set_bright',[100,'smooth',500], autoDisconnect = False, useExistingSocket = sx)
        time.sleep(0.5)