'''
Test Audiowall application.
===========================
'''

from kivy.app import App
from dps.audiowall.page import AudiowallPage

import globals   

class TestApp(App):
    def build(self):
        self.root = root = AudiowallPage(spacing=5, cols=3)
        return root

if __name__ == '__main__':
    globals.init()
    TestApp().run()
