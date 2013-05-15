'''
Audiowall Set. Made up of AudiowallPages.
============================================
'''

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from dps.audiowall.page import AudiowallPage

import globals

class AudiowallSet(BoxLayout):

    def __init__(self, **kwargs):
        super(AudiowallSet, self).__init__(**kwargs)
        self.pages = []
        self.container = Accordion()
        self.add_widget(self.container)
        self.register_event_type('on_add_page')
        for i in range(0,3,1):
            self.dispatch('on_add_page')

    def on_add_page(self, *largs):
        box = AccordionItem()
        page = AudiowallPage()
        box.add_widget(page)
        self.container.add_widget(box)
        self.pages.append(page)