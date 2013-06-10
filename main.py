'''
Test Audiowall application.
===========================
'''

from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from dps.audiowall.set import AudiowallSet
from dps.audioplayer.player import AudioPlayer

import json

import globals

class TestApp(App):
    def build(self):
        Config.set('graphics', 'width', '1024')
        Config.set('graphics', 'height', '768')
        json_file = open('audiowall.json','r')
        json_object = json.load(json_file)

        self.root = BoxLayout(orientation='horizontal')
        self.leftbox = BoxLayout(size_hint=(.55,1), orientation='vertical', spacing=10)
        self.root.add_widget(self.leftbox)

        self.player_1 = AudioPlayer()
        self.leftbox.add_widget(self.player_1)

        self.player_1.filename = 'http://dps-dev.radio.warwick.ac.uk/audio/index.php?md5=440fe45865147fd061f246711087ada7&token=3b976023f313bc143af6c16cb44c09'
        self.player_1.title = 'Go To Hell (For Heaven\'s Sake)'
        self.player_1.artist = 'Bring Me The Horizon'

        self.player_2 = AudioPlayer()
        self.leftbox.add_widget(self.player_2)

        self.player_2.filename = 'http://dps-dev.radio.warwick.ac.uk/audio/index.php?md5=91ee35d487d8f89c3cc051efe28938fa&token=3b976023f313bc143af6c16cb44c09'
        self.player_2.title = 'Get Lucky (Radio Edit) [feat. Pharrell Williams]'
        self.player_2.artist = 'Daft Punk'

        self.player_3 = AudioPlayer()
        self.leftbox.add_widget(self.player_3)

        self.player_3.filename = 'http://dps-dev.radio.warwick.ac.uk/audio/index.php?md5=61d0c1042bcae7d009a3bd8e5963e931&token=3b976023f313bc143af6c16cb44c09'
        self.player_3.title = 'The City (Extended Mix)'
        self.player_3.artist = 'Madeon'

        self.rightbox = BoxLayout(orientation='vertical', size_hint=(.45,1))
        self.root.add_widget(self.rightbox)

        self.primary_wall = AudiowallSet()
        i = 0
        for page in json_object:
            name = page.get('name')
            id = page.get('id')
            items = page.get('items')
            self.primary_wall.add_page(id,name)
            if items:
                for item in items:
                    fn = 'http://dps-dev.radio.warwick.ac.uk/audio/index.php?md5=%s&token=3b976023f313bc143af6c16cb44c09' % (item.get('audio'))
                    background = [int(item.get('background')[0])/float(255),int(item.get('background')[1])/float(255),int(item.get('background')[2])/float(255),1]
                    self.primary_wall.pages[i].buttons[int(item.get('item'))].title = item.get('text')
                    self.primary_wall.pages[i].buttons[int(item.get('item'))].background = background
                    self.primary_wall.pages[i].buttons[int(item.get('item'))].id = int(item.get('id'))
                    self.primary_wall.pages[i].buttons[int(item.get('item'))].filename = fn
            i += 1

        self.rightbox.add_widget(self.primary_wall)

        self.secondary_wall = AudiowallSet()
        i = 0
        #for fn in glob('/home/jonty/src/beemo/testaudio/*'):
        #    self.secondary_wall.pages[0].buttons[i].title = basename(fn[:-4]).replace('_', ' ')
        #    self.secondary_wall.pages[0].buttons[i].filename = fn
        #    i += 1
            
        self.rightbox.add_widget(self.secondary_wall)
        return self.root

if __name__ == '__main__':
    globals.init()
    TestApp().run()
