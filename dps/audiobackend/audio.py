'''
GStreamer audio plugin.  Plays any format commonly understood by GStreamer.
===========================================================================
'''

try:
    import pygst
    if not hasattr(pygst, '_gst_already_checked'):
        pygst.require('0.10')
        pygst._gst_already_checked = True
    import gst
except:
    raise

import sys
from kivy.logger import Logger
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, OptionProperty, NumericProperty

from kivy.support import install_gobject_iteration
install_gobject_iteration()

import globals

class Audio(EventDispatcher):
    source = StringProperty(None)
    output = StringProperty(None)
    device = StringProperty(None)
    _length = NumericProperty(None)
    state = OptionProperty('stop', options=('stop', 'play', 'pause', 'null'))
    level_left = NumericProperty(None)
    level_right = NumericProperty(None)

    def _get_filename(self):
        return self.source

    def __init__(self, **kwargs):
        self._pipeline = gst.Pipeline()

        bus = self._pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self._on_gst_message)

        self._decodebin = gst.element_factory_make('uridecodebin')
        self._decodebin.set_property('use-buffering', True)
        self._decodebin.set_property('buffer-size', 0)
        self._decodebin.set_property('buffer-duration', 200000000000)

        self._audioconvert = gst.element_factory_make('audioconvert')

        self._replaygain = gst.element_factory_make('rgvolume')
        self._replaygain.set_property('album-mode', False)
        self._replaygain.set_property('fallback-gain', -14)
        self._replaygain.set_property('pre-amp', 14)

        self._audioresample = gst.element_factory_make('audioresample')

        self._level = gst.element_factory_make('level', 'level')
        self._level.set_property('message', True)
        self._level.set_property('interval', 50000000)
        self._level.set_property('peak-falloff', 1000)
        self._level.set_property('peak-ttl', 50000000)

        self._tee = gst.element_factory_make('tee')

        self._fakesink = gst.element_factory_make('fakesink')
        self._fakesink.set_property('async', False)

        self.output = kwargs['output']
        self.device = kwargs['device']

        self._qaudiosink = gst.element_factory_make('queue')
        self._qaudiosink.set_property('silent', True)
        self._qaudiosink.set_property('max-size-buffers', 1)
        self._qaudiosink.set_property('leaky', True)

        if self.output == 'alsa':
            self._audiosink = gst.element_factory_make("alsasink")
            self._audiosink.set_property('device', self.device)
        elif self.output == 'jack':
            self._audiosink = gst.element_factory_make("jackaudiosink")
            self._audiosink.set_property('name', self.device)
        else:  
            Logger.error('GStreamer: Invalid sound output / device: %s / %s' % (self.output, self.device))
        self._audiosink.set_state(gst.STATE_NULL)
        self._audiosink.set_locked_state(True)
        
        self._pipeline.add(self._decodebin, self._audioconvert, self._replaygain, self._audioresample, self._level, self._tee, self._fakesink, self._qaudiosink, self._audiosink)

        gst.element_link_many(self._audioconvert, self._replaygain, self._audioresample, self._level, self._tee)
        self._decodebin.connect('pad-added', self._on_pad_added)

        self._tee.link(self._fakesink)
        self._tee.link(self._qaudiosink)

        self.register_event_type('on_play')
        self.register_event_type('on_stop')
        self.register_event_type('on_pause')
        self.register_event_type('on_loaded')
        self.register_event_type('on_level')
        super(Audio, self).__init__(**kwargs)
        
    def __del__(self):
        if self._pipeline is not None:
            self._pipeline.set_state(gst.STATE_NULL)

    def _on_pad_added(self, element, pad):
        if not self._audioconvert.get_pad('sink').is_linked():
            pad.link(self._audioconvert.get_pad('sink'))

    def _on_gst_message(self, bus, message):
        t = message.type
        s = message.src.get_name()
        if t == gst.MESSAGE_EOS:
            self.stop()
        elif t == gst.MESSAGE_ERROR:
            self._pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            Logger.error('AudioGstreamer: %s: %s' % (s,err))
            Logger.debug(str(debug))
            Logger.debug('Filename: %s' % self.filename)
            self._pipeline.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_BUFFERING:
            buffer = message.parse_buffering()
            #Logger.debug('Audio buffering: %s' % buffer)
            if(self._loading):
                if(buffer > 10):
                    if self._loading:
                        self.dispatch('on_loaded')
                        self._loading = False
        elif t == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()
            if (s == 'alsasink0'):
                Logger.debug('Audio state change: %s: %s -> %s (%s)' % (s, old, new, pending))
        elif t == gst.MESSAGE_ELEMENT:
            self.level_left = 36 - (message.structure['peak'][0] * -1)
            self.level_right = 36 - (message.structure['peak'][1] * -1)
            self.dispatch('on_level')

    def on_source(self, instance, filename):
        if filename is None:
            return
        self.filename = filename
        self.load()

    def _get_pos(self):
        if self._pipeline is not None:
            try:
                return self._pipeline.query_position(gst.Format(gst.FORMAT_TIME))[0] / 1000000000.
            except:
                pass
        return 0
    position = property(lambda self: self._get_pos())

    def _get_length(self):
        if self._pipeline is not None:
            if self._length is not None:
                return self._length
            else:
                try:
                    self._length = self._pipeline.query_duration(gst.Format(gst.FORMAT_TIME))[0] / 1000000000.
                    return self._length
                except:
                    pass
                return 0
    length = property(lambda self: self._get_length())

    def _get_buffer(self):
        if self._pipeline is not None:
            try:
                return self._buffer.get_property('current_level_time') / 1000000000.
            except:
                pass
        return 0
    buffer = property(lambda self: self._get_buffer())

    
    def load(self):
        self._loading = True;
        filepath = self.filename
        if filepath is None:
            return

        self._decodebin.set_property('uri', filepath)

        self._pipeline.set_state(gst.STATE_PAUSED)
        self.state = 'stop'

    def unload(self):
        self.stop()

        self._pipeline.set_state(gst.STATE_NULL)
        self.state = 'null'

    def play(self):
        if not self._pipeline:
            return
    
        self._audiosink.set_state(gst.STATE_PLAYING)

        if not self._audiosink.get_pad('sink').is_linked():
            self._qaudiosink.set_property('leaky', False)
            self._qaudiosink.link(self._audiosink)
        
        self._pipeline.set_state(gst.STATE_PLAYING)
        self.state = 'play'
        self.dispatch('on_play')

    def stop(self):
        if not self._pipeline:
            return

        if self._audiosink.get_pad('sink').is_linked():
            self._qaudiosink.set_property('leaky', True)
            self._qaudiosink.unlink(self._audiosink)

        self._audiosink.set_state(gst.STATE_READY)
        self._pipeline.set_state(gst.STATE_READY)

        self._pipeline.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
        self._pipeline.set_state(gst.STATE_PAUSED)
        self._audiosink.set_state(gst.STATE_NULL)
        self.state = 'stop'
        self.dispatch('on_stop')

    def pause(self):
        if not self._pipeline:
            return
        self._audiosink.set_state(gst.STATE_PAUSED)
        self._pipeline.set_state(gst.STATE_PAUSED)
        self.state = 'pause'
        self.dispatch('on_pause')

    def seek(self, position):
        if self._pipeline is None:
            return
        self._pipeline.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, position / 1000000000.)

    def on_play(self):
        pass

    def on_stop(self):
        pass
        
    def on_pause(self):
        pass
        
    def on_loaded(self):
        self.duration = self._get_length()
        pass

    def on_state(self, instance, state):
        pass

    def on_level(self):
        pass

