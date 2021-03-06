#!/usr/bin/env python2

# -*- coding: utf-8 -*-

# Copyright (c) 2012 Hugo Osvaldo Barrera <hugo@osvaldobarrera.com.ar>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

try:
    import alsaaudio
except:
    print "Error: need python-pyalsaaudio"
try:
    import pygtk
    import pynotify
    pygtk.require('2.0')
except:
    print "Error: need python-notify, python-gtk2 and gtk"


class VolumeNotification():
    """
    A libnotify notification, which displays the volume and shows several
    buttons to alter it further.
    """

    def __init__(self, cardindex):
        self.__cardindex = cardindex

        self.__popup = pynotify.Notification("Volume", str(self.get_volume())
                                             + "%", "audio-volume-medium")
        self.__popup.add_action("increase", "+", self.increase_volume)
        self.__popup.add_action("decrease", "-", self.decrease_volume)
        self.__popup.add_action("mute", "Mute", self.toggle_mute)
        self.__popup.show()

        self._mixer = alsaaudio.Mixer(cardindex=cardindex)

    def get_volume(self):
        # A new mixer need to be created every time, since otherwise it keeps
        # returning the same value (a bug in python2-alsaaudio?)
        return alsaaudio.Mixer(cardindex=self.__cardindex).getvolume()[0]

    def alter_volume(self, delta):
        previous_volume = self.get_volume()

        new_volume = long(previous_volume + long(delta))
        print 'Volume was {}, setting to : {}'.format(previous_volume,
                                                      new_volume)
        if new_volume > 100:
            new_volume = 100
        if new_volume < 0:
            new_volume = 0

        self.set_volume(new_volume)

    def set_volume(self, new_volume):
        self._mixer.setvolume(new_volume)
        self._update()

    def increase_volume(self, notification=None, action=None, data=None):
        self.alter_volume(3)

    def decrease_volume(self, notification=None, action=None, data=None):
        self.alter_volume(-3)

    def toggle_mute(self, notification=None, action=None, data=None):
        if self.is_muted():
            self._mixer.setmute(0)
            self._update()
        else:
            self._mixer.setmute(1)
            self._update()

    def is_muted(self):
        return self._mixer.getmute()[0] == 1

    def _update(self):
        if not self.is_muted():
            self.__popup.update("Volume", str(self.get_volume()) + "%",
                                "audio-volume-medium")
        else:
            self.__popup.update("Volume", str(self.get_volume()) + "% (Muted)",
                                "audio-volume-muted")
        self.__popup.show()
