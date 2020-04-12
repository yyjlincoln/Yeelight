import time
from devicesdef import WifiBulbConfig, WifiBulb
from discover import Discover

a = Discover(WifiBulbConfig)

discovered = a.discover()

for x in discovered:
    x = discovered[x]

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
