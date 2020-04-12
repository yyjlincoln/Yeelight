from devicesdef import WifiBulbConfig
from discover import Discover

a = Discover(WifiBulbConfig)

a.discover()
print(a.discovered)
import time

# for x in a.discovered:
#     print(x, a.discovered[x].Location)
#     sx = a.discovered[x]._connectToDevice()
#     a.discovered[x].sendCommand(1,'set_power',['on','smooth',5000], autoDisconnect=False, useExistingSocket = sx)
#     time.sleep(5)
#     for d in range(5):
#         res, sx = a.discovered[x].sendCommand(1,'set_bright',[1,'smooth',500], autoDisconnect = False, useExistingSocket = sx)
#         time.sleep(0.5)
#         res, sx = a.discovered[x].sendCommand(1,'set_bright',[100,'smooth',500], autoDisconnect = False, useExistingSocket = sx)
#         time.sleep(0.5)
#     a.discovered[x].sendCommand(1,'set_power',['off','smooth',5000], autoDisconnect=False, useExistingSocket = sx)

for x in a.discovered:

    x = a.discovered[x]

print(x.get_prop(['rgb']))
x.set_rgb(0, 153, 204)