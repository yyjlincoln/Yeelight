from abc import abstractclassmethod
import socket
import json

class YeelightBaseObject(object):
    'Yeelight Base Object'
    pass

class YeelightBaseException(Exception):
    'Yeelight Exception'
    pass

class YeelightDevice(YeelightBaseObject):
    'A Yeelight Device'
    def __init__(self, **kw):
        self.methods = []
        self.Location = ''
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
        tmp = self.Location.replace('yeelight://','')
        addr, port = tmp.split(':')
        port = int(port)

        # Perform connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        return s

    def sendCommand(self, id, method, params, autoDisconnect = True, useExistingSocket = False):
        assert isinstance(params, list)
        assert isinstance(id, int)
        assert isinstance(method, str)
        assert method in self.methods
        assert 'Location' in self.__dict__

        cmd = json.dumps({
            'id':id,
            'method':method,
            'params':params
        })
        cmd+='\r\n'

        # Initialize the connection
        if not useExistingSocket:
            s = self._connectToDevice()
        else:
            s = useExistingSocket

        s.send(cmd.encode())
        res = s.recv(2048)
        if autoDisconnect:
            s.shutdown(socket.SHUT_RDWR)
            s.close()
            s = None
        if res:
            return res, s
        else:
            return None, s

    pass

class YeelightDeviceConfiguration(YeelightBaseObject):
    'The Configuration of a Device.'
    pass