from discover import Discover
from music import MusicServer
from devicesdef import WifiBulbConfig

dev = Discover(WifiBulbConfig).discover()

dev = next(iter(dev.values())) # Get the first one

dev.set_power('on')

dev.set_ct_abx(5000)

dev.set_bright(100)

exit()

srv = MusicServer(port=8080)

srv.launch()

dev.set_music(1, '192.168.20.4',8080)

msc = srv.next_device(dev)

import random

for x in range(10000):
    msc.set_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255), wait = 10, smooth = False)

msc.disconnect_music()

srv.terminate()