import time
from devicesdef import WifiBulbConfig, WifiBulb
from discover import Discover

a = Discover(WifiBulbConfig)

a.discover()
print(a.discovered)

# for x in a.discovered:
#     print(x, a.discovered[x].Location)
#     sx = a.discovered[x]._connectToDevice()
#     a.discovered[x].sendCommand(1,'set_power',['on','smooth',5000], autoDisconnect=False, useExistingSocket = sx)
#     time.sleep(5)
#     for d in range(5):
#         res, sx = a.discovered[x].sendCommand(1,'set_bright',[1,'smooth',500], autoDisconnect = False, useExistingSocket = sx)
#         time.sleep(0.5)
#         res, sx = a.discovered[x].sendCommand(1,'set_bright',[100,'smooth',500], autoDisconnect = False, useExistingSocket = sx)
#         time.sleep(0.5)
#     a.discovered[x].sendCommand(1,'set_power',['off','smooth',5000], autoDisconnect=False, useExistingSocket = sx)

for x in a.discovered:

    x = a.discovered[x]

print(x.get_prop(['rgb']))
# x.set_power('on')
# x.set_ct_abx(6300)
# x.set_bright(100)
# x.set_bright(1)
# x.set_bright(100)
# x.set_power('off')
#     # x.set_rgb(16,79,162, duration = 2000)
#     # x.set_rgb(230,79,162, duration = 2000)
# x.toggle()
# print(x.toggle())
# x = WifiBulb()

x.set_power('on')
x.start_cf(0, 0, [
        {
            'duration': 3000,
            'mode': 'rgb',
            'red': 255,
            'green': 0,
            'blue': 0,
            'brightness': 100
        }, {
            'duration': 3000,
            'mode': 'rgb',
            'red': 0,
            'green': 255,
            'blue': 0,
            'brightness': 50
        }, {
            'duration': 3000,
            'mode': 'white',
            'colortemp': 2700,
            'brightness': 100
        }
])
time.sleep(20)
x.stop_cf()
x.set_rgb(255,255,0)
x.set_bright(100)
x.set_bright(1)
x.set_bright(100)
x.set_ct_abx(2700)
x.set_ct_abx(5400)
x.set_power('off')

# x.set_scene({
#     'class': 'cf',
    # 'flow': [
    #     {
    #         'duration': 3000,
    #         'mode': 'rgb',
    #         'red': 255,
    #         'green': 0,
    #         'blue': 0,
    #         'brightness': 100
    #     }, {
    #         'duration': 3000,
    #         'mode': 'rgb',
    #         'red': 0,
    #         'green': 255,
    #         'blue': 0,
    #         'brightness': 50
    #     }, {
    #         'duration': 3000,
    #         'mode': 'white',
    #         'colortemp': 2700,
    #         'brightness': 100
    #     }
    # ],
#     'count':2,
#     'action':2
# })

# print(x.start_cf(10, 0, [
#     {
#         'duration':3000,
#         'mode':'rgb',
#         'red':255,
#         'green':0,
#         'blue':0,
#         'brightness':100
#     },{
#         'duration':3000,
#         'mode':'rgb',
#         'red':0,
#         'green':255,
#         'blue':0,
#         'brightness':50
#     },{
#         'duration':3000,
#         'mode':'white',
#         'colortemp':2700,
#         'brightness':100
#     }
# ]))
