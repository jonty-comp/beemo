'''
Audiowall Set. Made up of AudiowallPages.
============================================
'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from dps.audiowall.page import AudiowallPage

import globals

class AudiowallSet(BoxLayout):

    def __init__(self, **kwargs):
        super(AudiowallSet, self).__init__(**kwargs)
        self.pages = []
        self.active_page = 1

        self._container = BoxLayout(orientation='vertical')
        self.add_widget(self._container)

        self._sm = ScreenManager()
        self._sm.transition = SlideTransition()
        self._sm.transition.duration = 0.3
        self._container.add_widget(self._sm)

        self._buttons = BoxLayout(orientation='horizontal', size_hint=(1,0.25))
        self._container.add_widget(self._buttons)

        self.previous = Button(text='<<')
        self.previous.bind(on_press=self.on_previous)
        self._buttons.add_widget(self.previous)

        self.pages_label = Label()
        self._buttons.add_widget(self.pages_label)

        self.next = Button(text='>>')
        self.next.bind(on_press=self.on_next)
        self._buttons.add_widget(self.next)

    def add_page(self, id, name):      
        screen = Screen()
        screen.name = id
        page = AudiowallPage()
        page.name = name
        screen.add_widget(page)
        self._sm.add_widget(screen)
        self.pages.append(page)
        self.pages_label.text = 'Page %i of %i' % (self.active_page, len(self.pages))

    def on_previous(self, *largs):
        self._sm.transition.direction = 'right'
        self._sm.current = self._sm.previous()
        self.active_page -= 1
        if(self.active_page == 0):
            self.active_page = len(self.pages)
        self.pages_label.text = 'Page %i of %i' % (self.active_page, len(self.pages))

    def on_next(self, *largs):
        self._sm.transition.direction = 'left'
        self._sm.current = self._sm.next()
        self.active_page += 1
        if(self.active_page > len(self.pages)):
            self.active_page = 1
        self.pages_label.text = 'Page %i of %i' % (self.active_page, len(self.pages))