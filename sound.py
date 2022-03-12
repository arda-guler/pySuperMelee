from pygame import mixer
import math

def init_sound():
    mixer.init(channels=2)
    mixer.set_num_channels(11)

def playSfx(track, channel=1, volume=1, loops=0):

    # failsafe
    if channel == 0:
        print("WARNING: Channel 0 is reserved for BGM!")

        # don't just quit the program due to a sound playing fail
        # try to find another available channel instead
        for i in range(1, 10):
            if not getChannelBusy(i):
                channel = i

        # no available channel to fallback?
        # well, we will have to interrupt one then...
        if channel == 0:
            channel = 1
    
    chn = mixer.Channel(channel)
    track_path = "data/sfx/" + str(track) + ".ogg"
    snd = mixer.Sound(track_path)
    chn.set_volume(volume)
    chn.play(snd, loops)

def playBGM(track, volume=1):
    chn = mixer.Channel(0)
    track_path = "data/bgm/" + str(track) + ".ogg"
    snd = mixer.Sound(track_path)
    chn.set_volume(volume)
    chn.play(snd, -1)

def stopChannel(channel):
    try:
        chn = mixer.Channel(channel)
        chn.stop()
    except IndexError:
        pass

def getChannelBusy(channel):
    try:
        chn = mixer.Channel(channel)
        return chn.get_busy()
    except IndexError:
        return False

def getVolumeAtDistance(dist):
    return min(1, 1/(dist**2))

def setChannelVolume(channel, volume_left, volume_right = None):
    chn = mixer.Channel(channel)

    if not volume_right:
        chn.set_volume(volume_left)
    else:
        # yeah, can also do panning!
        chn.set_volume(volume_left, volume_right)
