'''
Audiowall Page. Made up of AudiowallButtons.
============================================
'''

from kivy.uix.gridlayout import GridLayout
from dps.audiowall.button import AudiowallButton

import globals
from glob import glob

class AudiowallPage(GridLayout):

    def __init__(self, **kwargs):
        super(AudiowallPage, self).__init__(**kwargs)
        globals._available = True
        self.register_event_type('on_add_button')
        for fn in glob('/home/jonty/src/beemo/testaudio/*'):
            self._fn = fn
            self.dispatch('on_add_button')

    def on_add_button(self, *largs):
        btn = AudiowallButton()
        btn.filename = self._fn
        self.add_widget(btn)