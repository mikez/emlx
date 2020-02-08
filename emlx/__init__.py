# -*- coding: utf-8 -*-
"""

emlx - the lightweight parser for emlx files.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic usage:

    >>> import emlx
    >>> message = emlx.read("12345.emlx")
    >>> message.bytecount
    1781
    >>> message.data['Message-Id']
    '<07F45222-4A09-11EA-BBA5-5CF9389AFA5E@example.com>'
    >>> message.data.keys()
    ['From', 'Mime-Version', 'Content-Type', 'Subject', 'Date', ...]
    >>> message.plist
    {'date-received': 1581123200, 'flags': {'read': True, ...}, ...}

Inspired by:

    Karl Dubost - https://gist.github.com/karlcow/5276813
    Rui Carmo - https://the.taoofmac.com/space/blog/2008/03/03/2211
    Jamie Zawinski - https://www.jwz.org/blog/2005/07/emlx-flags/
"""

import email
import plistlib


APPLE_MESSAGE_FLAGS = [
    "read",
    "deleted",
    "answered",
    "encrypted",
    "flagged",
    "recent",
    "draft",
    "initial",
    "forwarded",
    "redirected",
    ("attachment_count", 6),
    ("priority_level", 7),
    "signed",
    "is_junk",
    "is_not_junk",
    ("font_size_delta", 3),
    "junk_mail_level_recorded",
    "highlight_text_in_toc",
]


class Emlx:
    """This class represents an emlx object.

    Main attributes:
    - `bytecount` (int)
    - `data` (`email.message.Message` from Python standard library)
    - `plist` (dict)
    """

    def __init__(self, filepath, plist_only=False):
        self.bytecount = 0
        self.data = None
        self.plist = None
        self.parse(filepath, plist_only)

    def parse(self, filepath, plist_only=False):
        """Parse an emlx file and update self."""
        with open(filepath, "rb") as file:
            self.bytecount = int(file.readline().strip())
            if plist_only:
                file.seek(self.bytecount, 1)
            else:
                self.data = email.message_from_bytes(file.read(self.bytecount))
            self.plist = plistlib.loads(file.read())
            flags = self.plist["flags"] = Emlx.decode_plist_flags(
                self.plist.get("flags", 0)
            )
            # Fix for "attachment_count" set to 63. Why is this?
            attachment_count = flags.get("attachment_count")
            if attachment_count == 63:
                del flags["attachment_count"]

    @staticmethod
    def decode_plist_flags(integer):
        """Decode flags of emlx plist given by `integer`.

        See: https://www.jwz.org/blog/2005/07/emlx-flags/
        """
        result = {}
        bits = bin(integer)
        index = 0
        for key in APPLE_MESSAGE_FLAGS:
            if isinstance(key, tuple):
                key, count = key
                value = int(bits[index - count : index], 2)
            else:
                value = bool(int(bits[index - 1]))
                count = 1
            if value:
                result[key] = value
            index -= count
        return result


def read(filepath, plist_only=False):
    """Read an emlx filepath and return an `Emlx` object."""
    return Emlx(filepath, plist_only=plist_only)
