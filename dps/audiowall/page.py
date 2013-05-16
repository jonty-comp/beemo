'''
Audiowall Page. Made up of AudiowallButtons.
============================================
'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty
from dps.audiowall.item import AudiowallItem

import globals

class AudiowallPage(BoxLayout):

    name = StringProperty(None)

    def __init__(self, **kwargs):
        super(AudiowallPage, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.buttons = []

        self.label = Label()
        self.label.size_hint = (1,0.1)
        self.add_widget(self.label)

        self.grid = GridLayout()
        self.grid.cols = 3
        self.add_widget(self.grid)

        for i in range(0,12,1):
            self.add_item()

    def add_item(self, *largs):
        btn = AudiowallItem()
        self.grid.add_widget(btn)
        self.buttons.append(btn)

    def on_name(self, instance, name):
        print self.name
        self.label.text = self.name