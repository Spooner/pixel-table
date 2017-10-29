from __future__ import absolute_import, division, print_function, unicode_literals

from twisted.protocols import amp
import json


class GetMode(amp.Command):
    arguments = []
    response = [
        (b'mode', amp.String()),
    ]


class SetMode(amp.Command):
    arguments = [
        (b'mode', amp.String()),
    ]
    response = []
    
    
class GetPixels(amp.Command):
    arguments = []
    response = [
        (b'pixels', amp.String()),
    ]


class GetModeValue(amp.Command):
    arguments = [
        (b'name', amp.String()),
    ]
    response = [
        (b'value', amp.String()),
    ]


class SetModeValue(amp.Command):
    arguments = [
        (b'name', amp.String()),
        (b'value', amp.String()),
    ]
    response = [
    ]


class PixelTableProtocol(amp.AMP):
    def get_mode(self):
        return {b'mode': self.app.mode}
    GetMode.responder(get_mode)
    
    def set_mode(self, mode):
        self.app.mode = mode
        return {}
    SetMode.responder(set_mode)

    def get_pixels(self):
        return {b'pixels': self.app.pixel_data.tobytes()}
    GetPixels.responder(get_pixels)

    def get_mode_value(self, name):
        assert name in self.app.mode.VALUES

        return json.dumps({b'value': getattr(self.app.mode, name)})
    GetModeValue.responder(get_mode_value)

    def set_mode_value(self, name, value):
        assert name in self.app.mode.VALUES
        
        value = json.loads(value)['value']
        setattr(self.app.mode, name, value)
    SetModeValue.responder(set_mode_value)
