'''
Test Audiowall application.
===========================
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from dps.audiowall.page import AudiowallPage

from glob import glob
import json
import uuid

import globals

class TestApp(App):
    def build(self):
        self.root = BoxLayout(orientation='horizontal')
        self.leftbox = BoxLayout(size_hint=(.6,1))
        self.root.add_widget(self.leftbox)

        self.rightbox = BoxLayout(orientation='vertical', size_hint=(.4,1))
        self.root.add_widget(self.rightbox)

        self.primary_wall = AudiowallPage()
        i = 0
        for fn in glob('/home/jonty/src/beemo/testaudio/*'):
            print "%i - %s" % (i, fn)
            self.primary_wall.buttons[i].filename = fn
            i += 1

        self.rightbox.add_widget(self.primary_wall)

        self.secondary_wall = AudiowallPage()
        i = 0
        for fn in glob('/home/jonty/src/beemo/testaudio/*'):
            print "%i - %s" % (i, fn)
            self.secondary_wall.buttons[i].filename = fn
            i += 1
            
        self.rightbox.add_widget(self.secondary_wall)
        return self.root

if __name__ == '__main__':
    globals.init()
    TestApp().run()
