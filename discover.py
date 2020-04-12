import socket
from socket import socket as Socket
from base import YeelightBaseObject, YeelightBaseException, YeelightDevice, YeelightDeviceConfiguration
from devicesdef import WifiBulb, WifiBulbConfig
import logger
from logger import log

class Discover(YeelightBaseObject):
    def __init__(self, YeelightDeviceConfigurationObject):
        self.host = YeelightDeviceConfigurationObject.host
        self.port = YeelightDeviceConfigurationObject.port
        self.st = YeelightDeviceConfigurationObject.deviceType
        self.createNew = YeelightDeviceConfigurationObject.createNew
        self.pk = YeelightDeviceConfigurationObject.primaryKey
        self._raw = YeelightDeviceConfigurationObject
        self.killswitch = False
        self.response = False
        self.discovered = {}

    def discover(self, retries = 10):
        msg = '\r\n'.join([
            f'M-SEARCH * HTTP/1.1',
            f'HOST: {self.host}:{self.port}',
            f'MAN: \"ssdp:discover\"',
            f'ST: {self.st}'
        ])
        s = Socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        logger.log('Now searching for devices...')

        counter = 0
        while True:
            s.sendto(msg.encode(), (self.host, self.port))
            logger.log('M-Search sent, awaiting response...')
            s.settimeout(1)
            while True:
                try:
                    if self.killswitch:
                        logger.log('Killswitch activated. Stop searching...')
                        break

                    res = s.recv(2048)
                    logger.log('Response received.')
                    self.response = True
                    self._handleResponse(res)
                except socket.timeout:
                    break
            counter += 1
            if counter > retries or self.response or self.killswitch:
                break
        
        if self.response:
            return self.discovered
        else:
            return {}
    
    def _handleResponse(self, res):
        res = self._parseHeaders(res)
        # SSDP - Location
        assert 'Location' in res
        # Yeelight specific
        assert self.pk in res
        supportedFunctions = res['support'].split(' ')
        res['methods'] = supportedFunctions

        self.discovered[res[self.pk]] = self.createNew(**res)
        logger.log('Device '+res[self.pk]+' added.')

    def _parseHeaders(self, res):
        res = res.decode().split('\r\n')
        parsed = {}
        for x in res:
            x = x.split(':', 1)
            try:
                parsed[x[0].strip()]=x[1].strip()
            except:
                continue
        return parsed
    
    def kill(self):
        self.killswitch = True

