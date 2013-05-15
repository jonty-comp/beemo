'''
Audiowall Page. Made up of AudiowallButtons.
============================================
'''

from kivy.uix.gridlayout import GridLayout
from dps.audiowall.button import AudiowallButton

import globals

class AudiowallPage(GridLayout):

    def __init__(self, **kwargs):
        super(AudiowallPage, self).__init__(**kwargs)
        self.cols = 3
        globals._available = True
        self.buttons = []
        self.register_event_type('on_add_button')
        for i in range(0,12,1):
            self.dispatch('on_add_button')

    def on_add_button(self, *largs):
        btn = AudiowallButton()
        self.add_widget(btn)
        self.buttons.append(btn)