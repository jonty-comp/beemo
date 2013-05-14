from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from os.path import basename

from dps.audioplayer.audio import Audio

import globals

class AudiowallButton(Button):

    filename = StringProperty(None)
    audio = ObjectProperty(None)
    title = StringProperty(None)
    background = ListProperty([1,1,1,1])
    
    def __init__(self, **kwargs):
        self.audio = Audio()
        super(AudiowallButton, self).__init__(**kwargs)

    def update_position(self, *largs):
        remaining = self.time_format(self.audio.length - self.audio.position)
        self.text = "PLAYING\n"+str(remaining)

    def on_filename(self, instance, fn):
        self._load()

    def _load(self, *largs):
        if(globals._available):
            globals._available = False
            self.audio.filetype = 'flac'
            self.audio.source = self.filename
            self.audio.bind(on_loaded=self.on_loaded)
        else:
            Clock.schedule_interval(self._load, 0.25)
        
    def on_loaded(self, *args):
        self.title=basename(self.filename[:-4]).replace('_', ' ') 
        self.text = self.title+"\n"+self.time_format(self.audio.length)
        self.audio.bind(on_play=self.on_play)
        self.audio.bind(on_stop=self.on_stop)
        Clock.unschedule(self._load)
        globals._available = True

    def on_press(self):
        if self.audio.state != 'stop':
            self.audio.stop()
        else:
            self.audio.play()
        
    def on_stop(self, *args):
        Clock.unschedule(self.update_position)
        self.text = self.title+"\n"+self.time_format(self.audio.length)
        self.background_color = self.background
        
    def on_play(self, *args):
        Clock.schedule_interval(self.update_position, 1/30.)
        self.background_color = (255,0,0,1)

    def time_format(self, time):
        time *= 100
        sec, ms = divmod(time, 100)
        min, sec = divmod(sec, 60)
        hr, min = divmod(min, 60)
        time = "%02i.%02i" % (sec, ms)
        if(min > 0):
            time = ("%02im " % min) + time
        if(hr > 0):
            time = ("%02ih " % hr) + time
        return time