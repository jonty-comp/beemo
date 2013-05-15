'''
Audiowall Page. Made up of AudiowallButtons.
============================================
'''

from kivy.uix.gridlayout import GridLayout
from dps.audiowall.item import AudiowallItem

import globals

class AudiowallPage(GridLayout):

    def __init__(self, **kwargs):
        super(AudiowallPage, self).__init__(**kwargs)
        self.cols = 3
        globals._available = True
        self.buttons = []
        self.register_event_type('on_add_item')
        for i in range(0,12,1):
            self.dispatch('on_add_item')

    def on_add_item(self, *largs):
        btn = AudiowallItem()
        self.add_widget(btn)
        self.buttons.append(btn)