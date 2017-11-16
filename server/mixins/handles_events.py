from __future__ import absolute_import, division, print_function, unicode_literals

import smokesignal


class HandlesEvents(object):
    def initialize_event_handlers(self):
        for handler_name in (a for a in dir(self) if a.startswith("on_")):
            smokesignal.on(handler_name[3:], getattr(self, handler_name))
