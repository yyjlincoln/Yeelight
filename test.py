from discover import Discover
from music import MusicServer
from devicesdef import WifiBulbConfig


def test():
    dev = Discover(WifiBulbConfig).discover()

    dev = next(iter(dev.values())) # Get the first one

    # dev.set_power('on', wait=False)

    # dev.set_ct_abx(5000)

    # dev.set_bright(1, wait=False)
    # dev.set_rgb(255,255,255)

    # dev.set_power('on')

    # dev.set_bright(1,wait=False)
    # dev.set_rgb(1,1,0)
    dev.set_bright(1)

    # dev.set_power('off')

    exit()



    srv = MusicServer(port=8080)

    srv.launch()

    dev.set_music(1, '192.168.20.4',8080)

    msc = srv.next_device(dev)

    import random

    # msc.start_cf(10, 0, [
    #     {
    #         'mode':'rgb',
    #         'duration':900,
    #         'brightness':100,
    #         'red':250,
    #         'green':221,
    #         'blue':5
    #     },{
    #         'mode':'rgb',
    #         'duration':900,
    #         'brightness':100,
    #         'red':250,
    #         'green':160,
    #         'blue':5            
    #     },{
    #         'mode':'rgb',
    #         'duration':900,
    #         'brightness':100,
    #         'red':250,
    #         'green':5,
    #         'blue':101
    #     },
    #     {
    #         'mode':'rgb',
    #         'duration':900,
    #         'brightness':100,
    #         'red':255,
    #         'green':0,
    #         'blue':0
    #     },{
    #         'mode':'rgb',
    #         'duration':900,
    #         'brightness':100,
    #         'red':0,
    #         'green':0,
    #         'blue':255
    #     }
    # ])

    # msc.start_cf(15,0,[
    #     {
    #         'mode':'rgb',
    #         'duration':500,
    #         'brightness':50,
    #         'red':255,
    #         'blue':0,
    #         'green':0
    #     },
    #     {
    #         'mode':'rgb',
    #         'duration':500,
    #         'brightness':50,
    #         'red':0,
    #         'blue':255,
    #         'green':0
    #     }
    # ])

    # msc.set_rgb()
    for x in range(300):
        msc.set_rgb(random.randint(1,255),random.randint(1,255),random.randint(1,255), wait = 10, smooth = False)

    msc.disconnect_music()

    dev.set_power('off')

    dev.set_power('on', wait = False)

    dev.set_ct_abx(5000)


    srv.terminate()

test()

