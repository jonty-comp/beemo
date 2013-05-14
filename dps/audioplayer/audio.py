'''
GStreamer audio plugin.  Plays any format commonly understood by GStreamer.
===========================================================================
'''

__all__ = ['Audio', 'AudioLoader']

try:
    import pygst
    if not hasattr(pygst, '_gst_already_checked'):
        pygst.require('0.10')
        pygst._gst_already_checked = True
    import gst
except:
    raise

import os
import sys
from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.utils import platform
from kivy.resources import resource_find
from kivy.properties import StringProperty, NumericProperty, OptionProperty, AliasProperty

from kivy.support import install_gobject_iteration
install_gobject_iteration()

class Audio(EventDispatcher):
    source = StringProperty(None)
    state = OptionProperty('stop', options=('stop', 'play', 'pause'))

    def _get_filename(self):
        return self.source

    def __init__(self, **kwargs):
        self._pipeline = gst.element_factory_make('playbin2')
        self._audiosink = gst.element_factory_make('autoaudiosink')

        self._pipeline.set_property('audio-sink', self._audiosink)

        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_gst_message)

        self.register_event_type('on_play')
        self.register_event_type('on_stop')
        self.register_event_type('on_pause')
        self.register_event_type('on_loaded')
        super(Audio, self).__init__(**kwargs)
        
    def __del__(self):
        if self._pipeline is not None:
            self._pipeline.set_state(gst.STATE_NULL)

    def _on_gst_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self._pipeline.set_state(gst.STATE_READY)
            self.stop()
        elif t == gst.MESSAGE_ERROR:
            self._pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            Logger.error('AudioGstreamer: %s' % err)
            Logger.debug(str(debug))
            self.stop()
        elif t == gst.MESSAGE_BUFFERING:
            buffer = message.parse_buffering()
            #Logger.debug('Audio buffering: %s\%' % buffer)
        elif t == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()
            #Logger.debug('Audio state change: %s -> %s (%s)' % (old, new, pending))
            if(self._loading):
                if(new == gst.STATE_READY):
                    self.dispatch('on_loaded')
                    self._loading = False

    def on_source(self, instance, filename):
        self.unload()
        if filename is None:
            return
        self.filename = filename
        self.load()

    def _get_pos(self):
        if self._pipeline is not None:
            if self._pipeline.get_state()[1] == gst.STATE_PLAYING:
                try:
                    return self._pipeline.query_position(gst.Format(gst.FORMAT_TIME))[0] / 1000000000.
                except:
                    pass
        return 0
    position = property(lambda self: self._get_pos())

    def _get_length(self):
        if self._pipeline is not None:
            if self._pipeline.get_state()[1] != gst.STATE_PLAYING:
                volume_before = self._pipeline.get_property('volume')
                self._pipeline.set_property('volume', 0)
                self._pipeline.set_state(gst.STATE_PLAYING)
                try:
                    self._pipeline.get_state()
                    return self._pipeline.query_duration(gst.Format(
                        gst.FORMAT_TIME))[0] / 1000000000.
                finally:
                    self._pipeline.set_state(gst.STATE_NULL)
                    self._pipeline.set_property('volume', volume_before)
            else:
                return self._pipeline.query_duration(gst.Format
                        (gst.FORMAT_TIME))[0] / 1000000000.
        return 0
    length = property(lambda self: self._get_length())

    
    def load(self):
        self.unload()
        self._loading = True;
        fn = self.filename
        if fn is None:
            return

        slash = ''
        if sys.platform in ('win32', 'cygwin'):
            slash = '/'

        if fn[0] == '/':
            filepath = 'file://' + slash + fn
        else:
            filepath = 'file://' + slash + os.path.join(os.getcwd(), fn)

        self._pipeline.set_property('uri', filepath)
        self._pipeline.set_state(gst.STATE_READY)

    def unload(self):
        self.stop()
        self._pipeline.set_state(gst.STATE_NULL)

    def play(self):
        if not self._pipeline:
            return
        self._pipeline.set_state(gst.STATE_PLAYING)
        self.state = 'play'
        self.dispatch('on_play')

    def stop(self):
        if not self._pipeline:
            return
        self._pipeline.set_state(gst.STATE_READY)
        self.state = 'stop'
        self.dispatch('on_stop')
        
    def pause(self):
        if not self._pipeline:
            return
        self._pipeline.set_state(gst.STATE_PAUSED)
        self.state = 'pause'
        self.dispatch('on_pause')

    def seek(self, position):
        if self._pipeline is None:
            return
        self._pipeline.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_SKIP, position / 1000000000.)

    def on_play(self):
        pass

    def on_stop(self):
        pass
        
    def on_pause(self):
        pass
        
    def on_loaded(self):
        pass
