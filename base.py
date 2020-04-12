from abc import abstractclassmethod
import socket
import json
import random


class YeelightBaseObject(object):
    'Yeelight Base Object'
    pass


class YeelightBaseException(Exception):
    'Yeelight Exception'
    pass


class YeelightUnexcepted(YeelightBaseException):
    'Unexcepted Error Occured'
    pass

class YeelightDeviceException(YeelightBaseException):
    'Exception from the device'
    pass


class YeelightDevice(YeelightBaseObject):
    'A Yeelight Device'

    def __init__(self, **kw):
        self.methods = []
        self.Location = ''
        self.props = {
            'power': {
                'argtype': str,
                'convert': str,
                'description': 'on: smart LED is turned on / off: smart LED is turned off'
            },
            'bright': {
                'argtype': int,
                'convert': int,
                'description': 'Brightness percentage. Range 1 ~ 100'
            },
            'ct': {
                'argtype': int,
                'convert': int,
                'description': 'Color temperature. Range 1700 ~ 6500(k)'
            },
            'rgb': {
                'argtype': int,
                'convert': int,
                'description': 'Color. Range 1 ~ 16777215'
            },
            'hue': {
                'argtype': int,
                'convert': int,
                'description': 'Hue. Range 0 ~ 359'
            },
            'sat': {
                'argtype': int,
                'convert': int,
                'description': 'Saturation. Range 0 ~ 100'
            },
            'color_mode': {
                'argtype': int,
                'convert': int,
                'description': '1: rgb mode / 2: color temperature mode / 3: hsv mode'
            },
            'flowing': {
                'argtype': int,
                'convert': int,
                'description': '0: no flow is running / 1:color flow is running'
            },
            'delayoff': {
                'argtype': int,
                'convert': int,
                'description': 'The remaining time of a sleep timer. Range 1 ~ 60 (minutes)'
            },
            'flow_params': {
                # TODO Clearify
                'argtype': list,
                'convert': list,
                'description': 'Current flow parameters (only meaningful when \'flowing\' is 1)'
            },
            'music_on': {
                'argtype': int,
                'convert': int,
                'description': '1: Music mode is on / 0: Music mode is off'
            },
            'name': {
                'argtype': str,
                'convert': str,
                'description': 'The name of the device set by “set_name” command'
            },
            'bg_power': {
                'argtype': str,
                'convert': str,
                'description': 'Background light power status'
            },
            'bg_flowing': {
                'argtype': int,
                'convert': int,
                'description': 'Background light is flowing'
            },
            'bg_flow_params': {
                # TODO Clearify
                'argtype': list,
                'convert': list,
                'description': 'Current flow parameters of background light'
            },
            'bg_ct': {
                'argtype': int,
                'convert': int,
                'description': 'Color temperature of background light'
            },
            'bg_lmode': {
                'argtype': int,
                'convert': int,
                'description': '1: rgb mode / 2: color temperature mode / 3: hsv mode'
            },
            'bg_bright': {
                'argtype': int,
                'convert': int,
                'description': 'Brightness percentage of background light'
            },
            'bg_rgb': {
                'argtype': int,
                'convert': int,
                'description': 'Color of background light'
            },
            'bg_hue': {
                'argtype': int,
                'convert': int,
                'description': 'Hue of background light'
            },
            'bg_sat': {
                'argtype': int,
                'convert': int,
                'description': 'Saturation of background light'
            },
            'nl_br': {
                'argtype': int,
                'convert': int,
                'description': 'Brightness of night mode light'
            },
            'active_mode': {
                'argtype': int,
                'convert': int,
                'description': '0: daylight mode / 1: moonlight mode (ceiling light only)'
            }
        }
        # Add attributes
        for x in kw:
            setattr(self, x, kw[x])

    def __str__(self):
        return str('YeelightDevice Object. This function should be overwritten.')

    def __repr__(self):
        # self.__dict__
        return str('YeelightDevice Object. This function should be overwritten.')

    def _connectToDevice(self):
        # Get the address of the light
        tmp = self.Location.replace('yeelight://', '')
        addr, port = tmp.split(':')
        port = int(port)

        # Perform connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        return s

    def sendCommand(self, method, params, id=0, autoDisconnect=True, useExistingSocket=False, autoIDVerification=True):
        assert isinstance(params, list)
        assert isinstance(id, int)
        assert isinstance(method, str)
        assert method in self.methods
        assert 'Location' in self.__dict__

        if autoIDVerification:
            id = random.randint(0, 1000)

        cmd = json.dumps({
            'id': id,
            'method': method,
            'params': params
        })
        cmd += '\r\n'

        # Initialize the connection
        if not useExistingSocket:
            s = self._connectToDevice()
        else:
            s = useExistingSocket

        s.send(cmd.encode())
        res = s.recv(2048)
        res = json.loads(res.decode())
        if autoIDVerification:
            assert 'id' in res
            if res['id'] != id:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                raise YeelightUnexcepted('ID Verification Failed.')
                # return None, s

        if autoDisconnect:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            s = None
        
        if 'error' in res:
            raise YeelightDeviceException('Device raised an exception ('+str(method)+'): '+ str(res['error']) + ' with original params '+str(params))

        if res:
            return res, s
        else:
            return None, s
        

    def get_prop(self, propname, autoDisconnect=True, useExistingSocket=False):
        r, sx = self.sendCommand('get_prop', list(
            propname), autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket)

        if len(r['result']) != len(propname):
            raise YeelightUnexcepted(
                'The length of propname does not equal to the length of result.')
        pack = {}
        for x in range(len(r['result'])):
            if propname[x] in self.props:
                # Convert Type
                pack[propname[x]] = self.props[propname[x]
                                               ]['convert'](r['result'][x])
            else:
                pack[propname[x]] = r['result'][x]

        return pack, sx

    def set_ct_abx(self, colortemp, smooth=True, duration=500, autoDisconnect=True, useExistingSocket=False):
        r, sx = self.sendCommand('set_ct_abx', [colortemp, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket)
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx

    def _set_rgb(self, rgbvalue, smooth=True, duration=500, autoDisconnect=True, useExistingSocket=False):
        # This is the original function for setrgb
        r, sx = self.sendCommand('set_rgb', [rgbvalue, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket)
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx

    def set_rgb(self, red, green, blue, smooth=True, duration=500, autoDisconnect=True, useExistingSocket=False):
        r, sx = self._set_rgb(red*65536 + green*256 + blue, smooth, duration, autoDisconnect = autoDisconnect, useExistingSocket = useExistingSocket)
        return r, sx


class YeelightDeviceConfiguration(YeelightBaseObject):
    'The Configuration of a Device.'
    pass
