import time
from devicesdef import WifiBulbConfig, WifiBulb
from discover import Discover

a = Discover(WifiBulbConfig)

discovered = a.discover()

for x in discovered:
    x = discovered[x]

# x.set_power('off')

# import random
# while True:
#     x.set_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255), smooth = False, duration = 50)
#     time.sleep(1)
# x.set_power('off')
# print(x.sendCommand('set_musi',[0]))
# 
# print(x.set_music(1, '192.168.20.4',54302))
# print(x.get_prop(['music_on']))
# print(x.set_music(0, None, None))

# x.set_power('off')

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
x.set_music(0)
# x.toggle()
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
