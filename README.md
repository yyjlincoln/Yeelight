# Yeelight LAN Control

## General Information

This is the controlling module for Yeelight devices. (Tested for Wifi_Bulb, though should work for all Yeelight devices)

## Functionalities

- Device discovery

- Music Mode support (where client quota does not apply)

- Simplified color flow data structure

- Simplified scene data structure

- API Server

## Supported Controlling Methods

This module includes the following functionalities (refer to documentation):

- get_prop - Retrieve current property of smart LED

- set_ct_abx - Change the color temperature of a smart LED

- set_rgb - Change the color of a smart LED

- set_hsv - Change the color of a smart LED

- set_bright - Change the brightness of a smart LED

- set_power - Switch on or off the smart LED (software managed on / off)

- toggle - Toggle the smart LED

- set_default - Save current state of smart LED in persistent memory

- start_cf - Start a color flow

- stop_cf - Stop a running color flow

- set_scene - Set the smart LED directly to specified state

- cron_add - Start a timer job on the smart LED

- set_music - Start or stop music mode on a device

## Usage

### Device Discovery

To discover devices, simply write:

    from discover import Discover
    from devicesdef import WifiBulbConfig
    Discoverer = Discover(WifiBulbConfig) # This discovers "WifiBulb" using "WifiBulbConfig" defined in devicesdef.py
    Devices = Discoverer.discover()

Alternative way:

    from discover import Discover
    from devicesdef import WifiBulbConfig
    Discoverer = Discover(WifiBulbConfig)
    Devices = Discoverer.discovered.copy()

Devices is a dictionary, which is structured as:

    Devices = {
        '0x00000000': <Yeelight.WifiBulb Object>,
        'DeviceID': <Yeelight.WifiBulb Object>,
        ...
    }

### Start Music Mode

To start music mode and connect to it, use the following code:

    # Assume that a WifiBulb object have been obtained from the previous device discovery procedure, and is stored as mainCtl
    # Assume that the IP address is 192.168.20.4

    # Launch the music server
    from music import MusicServer
    msrv = MusicServer(host = '0.0.0.0', port = 1080)
    msrv.launch()

    # Tell the device to connect
    mainCtl.set_music(1,'192.168.20.4',1080)

    # Accept the connection, obtain the musicCtl
    musicCtl = msrv.next_device(mainCtl)

    # Now control musicCtl as if it is mainCtl
    musicCtl.set_rgb(255,0,0) # Set the light to red

### Quick Demo

A well-commented demo can be found in run.py.

Here is a copy of the demo. Please be aware that this demo might not be the same as run.py.

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
