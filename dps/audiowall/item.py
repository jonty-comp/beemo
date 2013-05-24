'''
Audiowall Item. Plays audio when you press it.
==============================================
'''

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty

from dps.audiobackend.audio import Audio

import globals

class AudiowallItem(Button):

    id = NumericProperty(None)
    filename = StringProperty(None)
    audio = ObjectProperty(None)
    title = StringProperty(None)
    disabled_bg = ListProperty([1,1,1,0])
    background = ListProperty([1,1,1,1])
    
    def __init__(self, **kwargs):
        self.audio = Audio(output='alsa',device='pulse')
        super(AudiowallItem, self).__init__(**kwargs)

    def update_position(self, *largs):
        remaining = self.time_format(self.audio.length - self.audio.position)
        self.text = "PLAYING\n"+str(remaining)

    def on_filename(self, instance, fn):
        if(self.filename != ''):
            self._load()

    def _load(self, *largs):
        if(globals._available):
            globals._available = False
            self.audio.source = self.filename
            self.audio.bind(on_loaded=self.on_loaded)
        else:
            Clock.schedule_once(self._load, 0.1)

    def _unload(self, *largs):
        self.filename = ''
        self.audio.unload()
        self.background_color = self.disabled_bg
        self.text = ''
        self.audio.unbind(on_play=self.on_play)
        self.audio.unbind(on_stop=self.on_stop)
        
    def on_loaded(self, *args):
        self.text = self.title+"\n"+self.time_format(self.audio.length)
        self.background_color = self.background
        self.audio.bind(on_play=self.on_play)
        self.audio.bind(on_stop=self.on_stop)
        globals._available = True

    def on_press(self):
        if(self.filename != ''):
            if self.audio.state == 'play':
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