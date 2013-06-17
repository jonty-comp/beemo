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
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty, ObjectProperty, OptionProperty, NumericProperty

from dps.audiobackend.audio import Audio

import json
import globals

class AudioPlayer(BoxLayout):

    filename = StringProperty(None)
    audio = ObjectProperty(None)
    title = StringProperty(None)
    artist = StringProperty(None)
    time_mode = OptionProperty('remain', options=('elapsed','remain'))
    timer = StringProperty(None)
    _position = NumericProperty(0)

    def __init__(self, **kwargs):
        self.audio = Audio(output='alsa',device='pulse')
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

        self.topbox.inner.col2.time_mode = Button(text='REMAIN', halign='center')
        self.topbox.inner.col2.add_widget(self.topbox.inner.col2.time_mode)
        self.topbox.inner.col2.time_mode.bind(on_press=self.timemode)

        self.topbox.inner.col3 = BoxLayout(orientation='vertical', size_hint=(0.7,1))
        self.topbox.inner.add_widget(self.topbox.inner.col3)

        self.topbox.inner.col3.log = Button(text='Log this!')
        self.topbox.inner.col3.add_widget(self.topbox.inner.col3.log)

        self.topbox.inner.col3.load = Button(text='Load')
        self.topbox.inner.col3.add_widget(self.topbox.inner.col3.load)
        self.topbox.inner.col3.load.bind(on_press=self.loadnext)

        self.middlebox = BoxLayout(orientation='vertical',size_hint=(1,0.6))
        self.add_widget(self.middlebox)

        self.middlebox.progressbar = Slider()
        self.middlebox.add_widget(self.middlebox.progressbar)

        self.middlebox.level_l = ProgressBar()
        self.middlebox.level_l.max = 36
        self.middlebox.add_widget(self.middlebox.level_l)

        self.middlebox.level_r = ProgressBar()
        self.middlebox.level_r.max = 36
        self.middlebox.add_widget(self.middlebox.level_r)

        self.bottombox = BoxLayout(size_hint=(1,1))
        self.add_widget(self.bottombox)

        self.bottombox.stop = Button(text='Stop',size_hint=(0.3, 1))
        self.bottombox.add_widget(self.bottombox.stop)

        self.bottombox.playpause = Button(text='Play',size_hint=(0.3, 1))
        self.bottombox.add_widget(self.bottombox.playpause)

        self.bottombox.spacer = Button(size_hint=(0.6,1), background_color=(0,0,0,0))
        self.bottombox.add_widget(self.bottombox.spacer)
        
    def update_position(self, *largs):
        if(self.time_mode == 'elapsed'):
            self.timer = self.time_format(self.audio.position)
        else:
            self.timer = self.time_format(self.audio.length - self.audio.position)
        self.topbox.inner.col1.time.text = self.timer
        self.middlebox.progressbar.value = self.audio.position


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
        self.bottombox.playpause.unbind(on_press=self.playpause)
        self.bottombox.stop.unbind(on_press=self.stop)
        
    def on_loaded(self, *args):
        Clock.schedule_once(self.update_position)
        self.middlebox.progressbar.max = self.audio.length
        self.topbox.inner.col1.title.text = "Title: %s" % self.title
        self.topbox.inner.col1.artist.text = "Artist: %s" % self.artist
        self.bottombox.playpause.bind(on_press=self.playpause)
        self.bottombox.stop.bind(on_press=self.stop)
        self.audio.bind(on_play=self.on_play)
        self.audio.bind(on_pause=self.on_pause)
        self.audio.bind(on_stop=self.on_stop)
        self.audio.bind(on_level=self.on_level)
        self.bottombox.playpause.text = "Play"

    def on_stop(self, *args):
        Clock.unschedule(self.update_position)
        Clock.schedule_once(self.update_position)
        self.bottombox.playpause.text = "Play"
        self.update_position

    def on_pause(self, *args):
        Clock.unschedule(self.update_position)
        self.bottombox.playpause.text = "Play"
        
    def on_play(self, *args):
        Clock.schedule_interval(self.update_position, 1/30.)
        self.bottombox.playpause.text = "Pause"

    def on_level(self, *args):
        self.middlebox.level_l.value = self.audio.level_left
        self.middlebox.level_r.value = self.audio.level_right

    def playpause(self, *args):
        if(self.audio.state != 'play'):
			self.audio.play()
        else:
			self.audio.pause()

    def stop(self, *args):
        if(self.audio.state != 'stop'):
            self.audio.stop()

    def timemode(self, *args):
        if(self.time_mode == 'elapsed'):
            self.time_mode = 'remain'
            self.topbox.inner.col2.time_mode.text = "REMAIN"
        else:
            self.time_mode = 'elapsed'
            self.topbox.inner.col2.time_mode.text = "ELAPSED"
        Clock.schedule_once(self.update_position)

    def loadnext(self,*args):
        if(self.audio.state != 'play'):
            #if(self.audio.state != 'null'):
            self._unload()
            Clock.schedule_once(self.update_position)
            next_song_file = open('next_song.json','r')
            next_song_object = json.load(next_song_file)
            fn = 'http://dps-dev.radio.warwick.ac.uk/audio/index.php?md5=%s&token=3b976023f313bc143af6c16cb44c09' % (next_song_object["md5"])
            self.title = next_song_object['title']
            self.artist = next_song_object['artist']
            self.filename = fn

    def time_format(self, time):
        time *= 100
        sec, ms = divmod(time, 100)
        min, sec = divmod(sec, 60)
        hr, min = divmod(min, 60)
        time = "%02i:%02i:%02i" % (min, sec, ms)
        if(hr > 0):
            time = ("%02i." % hr) + time
        return time
