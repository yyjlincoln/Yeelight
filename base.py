from abc import abstractclassmethod

class YeelightBaseObject(object):
    'Yeelight Base Object'
    pass

class YeelightBaseException(Exception):
    'Yeelight Exception'
    pass

class YeelightDevice(YeelightBaseObject):
    'A Yeelight Device'
    def __init__(self, **kw):
        # Add attributes
        for x in kw:
            setattr(self, x, kw[x])
    
    # def __iter__(self):
    #     return iter(self.__dict__)
    
    def __str__(self):
        return str('YeelightDevice Object. This function should be overwritten.')
    
    def __repr__(self):
        # self.__dict__
        return str('YeelightDevice Object. This function should be overwritten.')

    pass

class YeelightDeviceConfiguration(YeelightBaseObject):
    'The Configuration of a Device.'
    pass