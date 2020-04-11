from base import YeelightBaseObject, YeelightDeviceConfiguration, YeelightDevice
from abc import abstractclassmethod

class WifiBulb(YeelightDevice):
    # Refer to YeelightDevice class.
    def __repr__(self):
        return 'Wifi Bulb'
    pass

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