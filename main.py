'''
Test Audiowall application.
===========================
'''

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from dps.audiowall.set import AudiowallSet

from glob import glob
from os.path import basename
import json

import globals

class TestApp(App):
    def build(self):
        self.root = BoxLayout(orientation='horizontal')
        self.leftbox = BoxLayout(size_hint=(.55,1))
        self.root.add_widget(self.leftbox)

        self.rightbox = BoxLayout(orientation='vertical', size_hint=(.45,1))
        self.root.add_widget(self.rightbox)

        self.primary_wall = AudiowallSet()
        i = 0
        for i in range(0,3,1):
            j = 0
            for fn in glob('/home/jonty/src/beemo/testaudio/*'):
                self.primary_wall.pages[i].buttons[j].title = basename(fn[:-4]).replace('_', ' ')
                self.primary_wall.pages[i].buttons[j].filename = fn
                j += 1
            i += 1

        self.rightbox.add_widget(self.primary_wall)

        self.secondary_wall = AudiowallSet()
        i = 0
        for fn in glob('/home/jonty/src/beemo/testaudio/*'):
            self.secondary_wall.pages[0].buttons[i].title = basename(fn[:-4]).replace('_', ' ')
            self.secondary_wall.pages[0].buttons[i].filename = fn
            i += 1
            
        self.rightbox.add_widget(self.secondary_wall)
        return self.root

if __name__ == '__main__':
    globals.init()
    TestApp().run()
