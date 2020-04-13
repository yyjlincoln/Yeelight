import flask
from flask import Flask, jsonify
from flask_cors import CORS
from apiauto import auto, r, MustHave
from discover import Discover
from base import YeelightUnexcepted
from devicesdef import WifiBulb, WifiBulbConfig
from music import MusicServer
import logger
import base64, json
import socket

app = Flask(__name__)

devicesMapping = {
    'wifibulb': WifiBulbConfig
}

lastDiscovery = None
references = {}

msrv = MusicServer(port = 10800)
msrv.launch()

def discoverDevice(deviceConfig):
    global lastDiscovery
    lastDiscovery = Discover(deviceConfig)
    return lastDiscovery.discover()


discoverDevice(WifiBulbConfig)


@app.route('/discover')
@auto(devicetype='wifibulb')
def discover(devicetype):
    if devicetype in devicesMapping:

        d = discoverDevice(devicesMapping[devicetype])
        for x in d:
            d[x] = str(d[x])

        return r(0, devices=d)
    return r(-1, message='Device not defined.')


def getDeviceByID(deviceID):
    if lastDiscovery == None:
        logger.log('Not discovered')
        return False
        # return r(-1, message = 'Not discovered.')
    if deviceID in lastDiscovery.discovered:
        return lastDiscovery.discovered[deviceID]
    if deviceID in references:
        return references[deviceID]


@app.route('/get_prop')
@auto(device=MustHave(), propname='not_exist', wait=False)
def get_prop(device, propname='not_exist', wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.get_prop([propname], wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/set_ct_abx')
@auto(device=MustHave(), colortemp=2700, smooth=True, duration=500, wait=False)
def set_ct_abx(device, colortemp, smooth, duration, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_ct_abx(colortemp, smooth, duration, wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/set_rgb')
@auto(device=MustHave(), red=MustHave(), green=MustHave(), blue=MustHave(), smooth=True, duration=500, wait=False)
def set_rgb(device, red, blue, green, smooth, duration, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_rgb(red, green, blue, smooth, duration, wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/set_hsv')
@auto(device=MustHave(), hue=MustHave(), sat=MustHave(), smooth=True, duration=500, wait=False)
def set_hsv(device, hue, sat, smooth, duration, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_hsv(hue, sat, smooth, duration, wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/set_bright')
@auto(device=MustHave(), brightness=MustHave(), smooth=True, duration=500, wait=False)
def set_bright(device, brightness, smooth, duration, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_bright(brightness, smooth, duration, wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/set_power')
@auto(device=MustHave(), power=MustHave(), smooth=True, duration=500, wait=False)
def set_power(device, power, smooth, duration, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_power(power, smooth, duration, wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/toggle')
@auto(device=MustHave(), wait=False)
def toggle(device, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.toggle(wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')


@app.route('/set_default')
@auto(device=MustHave(), wait=False)
def set_default(device, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_default(wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')

@app.route('/start_cf')
@auto(device=MustHave(), count=MustHave(), action=0 , flow=MustHave(), wait=False)
def start_cf(device,count, action, flow, wait=False):
    dev = getDeviceByID(device)
    if dev:
        try:
            flow = json.loads(base64.b64decode(flow))
        except:
            return r(-3, message = 'Invalid flow. Flow must be jsonified, then encoded using base64.')

        st, sx = dev.start_cf(count, action, flow, wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')

@app.route('/stop_cf')
@auto(device=MustHave(), wait=False)
def stop_cf(device, wait=False):
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.stop_cf(wait=wait)
        return r(0, result=st, message='success' if st else 'failed')
    return r(-1, message='Device not found')

@app.route('/set_music')
@auto(device=MustHave(), action = MustHave(), wait=False)
def set_music(device,action, wait=False):
    global references
    dev = getDeviceByID(device)
    if dev:
        st, sx = dev.set_music(action, host=socket.gethostbyname(socket.gethostname()), port=10800, wait=wait)
        if st:
            hdlr = msrv.next_device(dev)
            references[dev.id + '::musicon'] = hdlr
            return r(0, message = 'success', reference = dev.id + '::musicon')
        return r(-1, message = 'request failed')
    return r(-1, message='Device not found')

@app.route('/cool')
@auto(device=MustHave())
def beCool(device):
    dev = getDeviceByID(device)

    if dev:
        import test
        test.test()
    return r(0, message="cool")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
