from base import YeelightBaseObject, YeelightDeviceConfiguration, YeelightDevice
from abc import abstractclassmethod

class WifiBulb(YeelightDevice):
    # Refer to YeelightDevice class.
    def __init__(self, **kw):
        self.id = None
        self.musicMode = False
        super().__init__(**kw)

    def __repr__(self):
        return f'<Wifi Bulb Object: {str(self.id)}, Music {"ON" if self.musicMode else "OFF"}>'

    def __str__(self):
        return f'<Wifi Bulb Object: {str(self.id)}, Music {"ON" if self.musicMode else "OFF"}>'


class WifiBulbConfig(YeelightDeviceConfiguration):
    deviceType = 'wifi_bulb'
    host = '239.255.255.250'
    port = 1982
    primaryKey = 'id' # This ensures that each device is unique.
    createNew = WifiBulb


# WifiBulb = {
#     'deviceType':'wifi_bulb',
#     'host':'239.255.255.250',
#     'port':1982
# }