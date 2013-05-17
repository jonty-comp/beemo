'''
Audio Player. Plays audio with a nice UI.
==============================================
'''

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.properties import StringProperty, ObjectProperty, ListProperty

from dps.audiobackend.audio import Audio

import globals

class AudioPlayer(BoxLayout):

    filename = StringProperty(None)
    audio = ObjectProperty(None)
    title = StringProperty(None)
    artist = StringProperty(None)

    def __init__(self, **kwargs):
        self.audio = Audio()
        super(AudioPlayer, self).__init__(**kwargs)

        self.orientation = 'vertical'

        self.topbox = BoxLayout(size_hint=(1,1))
        self.add_widget(self.topbox)

        self.topbox.inner = BoxLayout(orientation='horizontal')
        self.topbox.add_widget(self.topbox.inner)

        self.topbox.inner.col1 = BoxLayout(orientation='vertical')
        self.topbox.inner.add_widget(self.topbox.inner.col1)

        self.topbox.inner.col1.title = Label(text='Title: ', font_size='20sp', size_hint=(None, 1))
        self.topbox.inner.col1.title.bind(texture_size=self.topbox.inner.col1.title.setter('size'))
        self.topbox.inner.col1.add_widget(self.topbox.inner.col1.title)

        self.topbox.inner.col1.artist = Label(text='Artist: ', font_size='20sp', size_hint=(None, 1))
        self.topbox.inner.col1.artist.bind(texture_size=self.topbox.inner.col1.artist.setter('size'))
        self.topbox.inner.col1.add_widget(self.topbox.inner.col1.artist)

        self.topbox.inner.col1.time = Label(text='00:00:00', font_size='40sp', size_hint=(None, 1))
        self.topbox.inner.col1.time.bind(texture_size=self.topbox.inner.col1.time.setter('size'))
        self.topbox.inner.col1.add_widget(self.topbox.inner.col1.time)

        self.topbox.inner.col2 = BoxLayout(orientation='vertical', size_hint=(0.4,1))
        self.topbox.inner.add_widget(self.topbox.inner.col2)

        self.topbox.inner.col2.spacer = Label(text='')
        self.topbox.inner.col2.add_widget(self.topbox.inner.col2.spacer)

        self.topbox.inner.col2.time_mode = Button(text='ELAPSED', halign='center')
        self.topbox.inner.col2.add_widget(self.topbox.inner.col2.time_mode)

        self.topbox.inner.col3 = BoxLayout(orientation='vertical', size_hint=(0.7,1))
        self.topbox.inner.add_widget(self.topbox.inner.col3)

        self.topbox.inner.col3.log = Button(text='Log this!')
        self.topbox.inner.col3.add_widget(self.topbox.inner.col3.log)

        self.topbox.inner.col3.load = Button(text='Load')
        self.topbox.inner.col3.add_widget(self.topbox.inner.col3.load)

        self.middlebox = BoxLayout(size_hint=(1,0.6))
        self.add_widget(self.middlebox)

        self.middlebox.progressbar = Slider()
        self.middlebox.add_widget(self.middlebox.progressbar)

        self.bottombox = BoxLayout(size_hint=(1,1))
        self.add_widget(self.bottombox)

        self.bottombox.stop = Button(text='Stop',size_hint=(0.3, 1))
        self.bottombox.add_widget(self.bottombox.stop)

        self.bottombox.playpause = Button(text='Play',size_hint=(0.3, 1))
        self.bottombox.add_widget(self.bottombox.playpause)

        self.bottombox.spacer = Button(size_hint=(0.6,1), background_color=(0,0,0,0))
        self.bottombox.add_widget(self.bottombox.spacer)

    def update_position(self, *largs):
        elapsed = self.time_format(self.audio.position)
        remaining = self.time_format(self.audio.length - self.audio.position)

    def on_filename(self, instance, fn):
        if(self.filename != ''):
            self._load()

    def _load(self, *largs):
        self.audio.source = self.filename
        self.audio.bind(on_loaded=self.on_loaded)

    def _unload(self, *largs):
        self.filename = ''
        self.audio.unload()
        self.text = ''
        self.audio.unbind(on_play=self.on_play)
        self.audio.unbind(on_stop=self.on_stop)
        
    def on_loaded(self, *args):
        self.audio.bind(on_play=self.on_play)
        self.audio.bind(on_stop=self.on_stop)

    def on_press(self):
        if(self.filename != ''):
            if self.audio.state == 'play':
                self.audio.stop()
            else:
                self.audio.play()
        
    def on_stop(self, *args):
        Clock.unschedule(self.update_position)
        
    def on_play(self, *args):
        Clock.schedule_interval(self.update_position, 1/30.)

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