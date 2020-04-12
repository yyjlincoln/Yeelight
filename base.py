from abc import abstractclassmethod
import socket
import json
import random
import time


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
        self.musicMode = False
        self.musicCtl = None # This should be a socket object.
        # On music mode, the connection will not be closed. Other connection params will be ignored.
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

    def sendCommand(self, method, params, id=0, autoDisconnect=True, useExistingSocket=False, autoIDVerification=True, wait = 0):
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

        # Choose the socket
        if self.musicMode:
            # Music
            s = self.musicCtl
        else:
            # Initialize the connection
            if not useExistingSocket:
                s = self._connectToDevice()
            else:
                s = useExistingSocket

        s.send(cmd.encode())

        # No response in musicMode, return.

        if self.musicMode:
            return None, s

        flag = False
        while True:
            resd = s.recv(2048).decode().split('\r\n')
            print(resd)
            for x in resd:
                if x:
                    res = json.loads(x)
                    if 'id' in res:
                        flag = True
                        # Found a valid response in overlapping responses.
                        break
        
            if flag:
                break


        if autoIDVerification:
            assert 'id' in res
            if res['id'] != id:
                # s.shutdown(socket.SHUT_RDWR)
                # s.close()
                raise YeelightUnexcepted('ID Verification Failed.')
                # return None, s
        
        if autoDisconnect and not self.musicMode:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            s = None
        
        if 'error' in res:
            raise YeelightDeviceException('Device raised an exception ('+str(method)+'): '+ str(res['error']) + ' with original params '+str(params))
        
        time.sleep(wait * 0.001)
        if res:
            return res, s
        else:
            return None, s
        

    def get_prop(self, propname, autoDisconnect=True, useExistingSocket=False, wait = True):
        r, sx = self.sendCommand('get_prop', list(
            propname), autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)

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

    def set_ct_abx(self, colortemp, smooth=True, duration=500, autoDisconnect=True, useExistingSocket=False, wait = True):
        r, sx = self.sendCommand('set_ct_abx', [colortemp, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = duration if wait else 0)
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx

    def _set_rgb(self, rgbvalue, smooth=True, duration=500, autoDisconnect=True, useExistingSocket=False, wait = True):
        # This is the original function for setrgb
        r, sx = self.sendCommand('set_rgb', [rgbvalue, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = duration if wait else 0)
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx

    def set_rgb(self, red, green, blue, smooth=True, duration=500, autoDisconnect=True, useExistingSocket=False, wait = True):
        r, sx = self._set_rgb(red*65536 + green*256 + blue, smooth, duration, autoDisconnect = autoDisconnect, useExistingSocket = useExistingSocket, wait=wait)
        return r, sx
    
    def set_hsv(self, hue, sat, smooth = True, duration = 500, autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('set_hsv', [hue, sat, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = duration if wait else 0)       
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def set_bright(self, brightness, smooth = True, duration = 500, autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('set_bright', [brightness, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = duration if wait else 0)       
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx

    def set_power(self, power, mode = 0, smooth = True, duration = 500, autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('set_power', [power, 'smooth' if smooth else 'sudden', duration if duration >=
                                                30 else 30, mode], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = duration if wait else 0)       
        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def toggle(self, autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('toggle', [], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 30 if wait else 0)       

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def set_default(self, autoDisconnect = True, useExistingSocket = False, wait = True):
        # Save the current state
        r, sx = self.sendCommand('set_default', [], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)       

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def _start_cf(self, count, action, flow_expression ,autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('start_cf', [count, action, flow_expression], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)       

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def parse_flow(self, flow):
        '''
        Parse color flow object.

        Example of a flow object:

        flow = [
            {
                'duration': 30,
                'mode':'rgb / white / sleep',
                'red':0,
                'green':0,
                'blue':0,
                'colortemp':0,
                'brightness':0
            }
        ]
        '''
        final = []
        for x in flow:
            # if 'duration' not in x:
            #     raise YeelightUnexcepted('No duration param. Invalid flow.')
            # if 'mode'

            assert 'duration' in x
            assert 'mode' in x
            assert 'brightness' in x

            if x['duration'] <= 30:
                x['duration'] = 30

            final.append(str(x['duration']))
            
            if x['mode']=='rgb':
                assert 'red' in x
                assert 'green' in x
                assert 'blue' in x
                final.append(str(1)) # RGB
                final.append(str(x['red']*65536 + x['green']*256 + x['blue'])) #Value
            elif x['mode']=='white':
                assert 'colortemp' in x
                final.append(str(2))
                final.append(str(x['colortemp']))
            elif x['mode']=='sleep':
                final.append(str(7))
                final.append(str(0)) # Ignored
            
            final.append(str(x['brightness']))

        strfinal = ', '.join(final)
        return strfinal

    def start_cf(self, count, action, flow, autoDisconnect = True, useExistingSocket = False, wait = True):
        flowparsed = self.parse_flow(flow)
        return self._start_cf(count, action, flowparsed, autoDisconnect = autoDisconnect, useExistingSocket = useExistingSocket, wait = wait)
    
    def stop_cf(self, autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('stop_cf', [], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)       

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx        
    
    def _set_scene(self, sclass, val1, val2, val3=None, autoDisconnect = True, useExistingSocket = False, wait = True):
        if val3:
            r, sx = self.sendCommand('set_scene', [sclass, val1, val2, val3], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)
        else:
            r, sx = self.sendCommand('set_scene', [sclass, val1, val2], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def parse_scene(self, scene):
        '''
        Process scene object

        Example Scene:

        scene = {
            'class':'cf',
            'flow':[
                # Flow Object
            ],
            'count':10,
            'action':0
        }

        scene = {
            'class': 'color',
            'red':255,
            'green':255,
            'blue':255,
            'brightness':70
        }


        '''
        assert 'class' in scene
        if scene['class']=='color':
            assert 'red' in scene
            assert 'green' in scene
            assert 'blue' in scene
            assert 'brightness' in scene
            r,g,b,br = scene['red'], scene['green'], scene['blue'], scene['brightness']
            return scene['class'], r*65536 + g*256 + b, br, None
        elif scene['class']=='hsv':
            assert 'hue' in scene
            assert 'sat' in scene
            assert 'brightness' in scene
            return scene['class'], scene['hue'], scene['sat'], scene['brightness']
        elif scene['class']=='ct':
            assert 'colortemp' in scene
            assert 'brightness' in scene
            return scene['class'], scene['colortemp'], scene['brightness'], None
        elif scene['class']=='cf':
            assert 'flow' in scene
            assert 'count' in scene
            assert 'action' in scene
            flow = self.parse_flow(scene['flow'])
            return scene['class'], scene['count'], scene['action'], flow
        elif scene['class']=='auto_delay_off':
            assert 'brightness' in scene
            assert 'delay' in scene
            return scene['class'], scene['brightness'], scene['delay'], None
        else:
            raise YeelightUnexcepted('Can not match class.')

    def set_scene(self, scene,  autoDisconnect = True, useExistingSocket = False, wait = True):
        sclass, val1, val2, val3 = self.parse_scene(scene)
        return self._set_scene(sclass, val1, val2, val3, autoDisconnect = autoDisconnect, useExistingSocket = useExistingSocket, wait = wait)
    
    def _cron_add(self, stype, minutes,  autoDisconnect = True, useExistingSocket = False, wait = True):
        'Currently type can only be 0 - power off'
        r, sx = self.sendCommand('cron_add', [stype, minutes], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)       

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
    
    def delay_off(self, minutes):
        return self._cron_add(0, minutes)
    
    # Cron_get
    # Cron_del
    # Set_adjust
    # Set_name
    # bg_set_xx
    # bg_toggle
    # dev_toggle
    # adjust_bright
    # adjust_ct
    # adjust_color
    # bg_adjust_xx

    def set_music(self, action, host, port, autoDisconnect = True, useExistingSocket = False, wait = True):
        r, sx = self.sendCommand('set_music', [action, host, port], autoDisconnect=autoDisconnect, useExistingSocket=useExistingSocket, wait = 0 if wait else 0)       

        if r:
            if r['result'][0] == 'ok':
                return True, sx
        return False, sx
class YeelightDeviceConfiguration(YeelightBaseObject):
    'The Configuration of a Device.'
    pass
