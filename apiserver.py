import flask
from flask import Flask, jsonify
from flask_cors import CORS
from apiauto import auto, r, MustHave
from discover import Discover
from base import YeelightUnexcepted
from devicesdef import WifiBulb, WifiBulbConfig
import logger

app = Flask(__name__)

devicesMapping = {
    'wifibulb':WifiBulbConfig
}

lastDiscovery = None


def discoverDevice(deviceConfig):
    global lastDiscovery
    lastDiscovery = Discover(deviceConfig)
    return lastDiscovery.discover()

discoverDevice(WifiBulbConfig)


@app.route('/discover')
@auto(devicetype = 'wifibulb')
def discover(devicetype):
    if devicetype in devicesMapping:

        d = discoverDevice(devicesMapping[devicetype])
        for x in d:
            d[x] = str(d[x])

        return r(0, devices = d)
    return r(-1, message = 'Device not defined.')

def getDeviceByID(deviceID):
    if lastDiscovery == None:
        logger.log('Not discovered')
        return False
        # return r(-1, message = 'Not discovered.')
    if deviceID in lastDiscovery.discovered:
        return lastDiscovery.discovered[deviceID]

@app.route('/toggle')
@auto(device = MustHave())
def toggle(device):
    dev = getDeviceByID(device)
    if dev:
        stat, sx = lastDiscovery.discovered[device].toggle()
        return r(0, result = stat, message = 'success' if stat else 'failed')
    else:
        return r(-1, message = 'Device not found.')

@app.route('/set_rgb')
@auto(device = MustHave(),red = MustHave(), green = MustHave(), blue = MustHave(), smooth = True, duration = 500)
def set_rgb(device, red, blue, green, smooth, duration):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_rgb(red, green, blue, smooth, duration)
        return r(0, result = st, message = 'success' if st else 'failed')
    return r(-1, message = 'Device not found')
    
@app.route('/set_colortemp')
@auto(device = MustHave(), colortemp = 2700 , smooth = True, duration = 500)
def set_colortemp(device, colortemp, smooth, duration):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_ct_abx(colortemp, smooth, duration)
        return r(0, result = st, message = 'success' if st else 'failed')
    return r(-1, message = 'Device not found')

@app.route('/cool')
@auto(device = MustHave())
def beCool(device):
    dev = getDeviceByID(device)

    if dev:
        import test
        test.test()
    return r(0, message = "cool")

app.run(host='0.0.0.0')