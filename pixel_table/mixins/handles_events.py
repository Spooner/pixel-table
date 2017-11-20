from __future__ import absolute_import, division, print_function, unicode_literals

from functools import partial

import smokesignal


class HandlesEvents(object):
    def initialize_event_handlers(self):
        for handler_name in (a for a in dir(self) if a.startswith("on_")):
            smokesignal.on(handler_name[3:], partial(self._handle_event, handler_name))

    def _handle_event(self, handler_name, *args, **kwargs):
        if getattr(self, "_is_destroyed", False):
            return

        getattr(self, handler_name)(*args, **kwargs)

    @staticmethod
    def emit(event, *args, **kwargs):
        smokesignal.emit(event, *args, **kwargs)
