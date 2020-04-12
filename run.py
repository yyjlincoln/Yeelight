import time
from devicesdef import WifiBulbConfig, WifiBulb
from discover import Discover
from music import MusicServer
import logger

# Discover a device
Discoverer = Discover(WifiBulbConfig)
Devices = Discoverer.discover()
if Devices:
    # Pick the first one
    Device = next(iter(Devices.values())) 
    
    # Turn on the first device
    Device.set_power('on')

    # Set the first device to white, 5400k colortemp
    Device.set_ct_abx(5400)

    # Set the first device to red
    Device.set_rgb(255,0,0)

    # Set the first device to blue
    Device.set_rgb(0,0,255)

    # Start a color flow
    flow = [
        {
            'duration':500,
            'mode':'rgb',
            'red':255,
            'green':0,
            'blue':0,
            'brightness':100
        },{
            'duration':500,
            'mode':'rgb',
            'red':0,
            'green':0,
            'blue':255,
            'brightness':100
        }
    ]
    Device.start_cf(10,0,flow)

    # Wait for the color flow to finish
    time.sleep(5)

    # Before music mode, need to start the server
    Server = MusicServer(port = 10800)
    Server.launch()

    # Now, tell the device to connect
    Device.set_music(1,'192.168.20.4', 10800)

    # Then, at the server side, we need to get the connected device
    MusicControlSocket = Server.next_device(Device)

    # Try something with music mode
    import random
    for x in range(10):
        MusicControlSocket.set_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255))
    
    # Stop music mode
    Device.set_music(0)

    # Toggle the device (which should turn it off)
    Device.toggle()

else:
    logger.info('No device found!')