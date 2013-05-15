'''
Test Audiowall application.
===========================
'''

from kivy.app import App
from dps.audiowall.page import AudiowallPage

from glob import glob

import globals   

class TestApp(App):
    def build(self):
        self.root = root = AudiowallPage()
        i = 0
        for fn in glob('/home/jonty/src/beemo/testaudio/*'):
            print "%i - %s" % (i, fn)
            root.buttons[i].filename = fn
            i += 1
        return root

if __name__ == '__main__':
    globals.init()
    TestApp().run()
