# -*- coding: utf-8 -*-

"""
emlx.emlx
~~~~~~~~~~~~

This module implements the Emlx object and helper methods.
"""

import email
from email.header import decode_header
from email.header import make_header
import email.message
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


class Emlx(email.message.Message):
    """This class represents an emlx object.

    It's implemented as an extension of `email.message.Message`
    from the Python standard library.
    """

    def __init__(self):
        super().__init__()

        # MIME message byte length.
        self.bytecount = 0

        # Dictionary of MIME message headers, e.g., 'From' and 'Date'.
        # See: https://en.wikipedia.org/wiki/MIME#MIME_header_fields
        self.headers = None

        # String of 'Message-ID' header if present. Case-insentive match.
        # See: https://tools.ietf.org/html/rfc2392
        self.id = None

        # Message url if available.
        # See: https://daringfireball.net/2007/12/message_urls_leopard_mail
        self.url = None

        # Dictionary of plist included by Mail.app.
        self.plist = {}

        # Dictionary of flags set by Mail.app, e.g., 'read' or 'answered'.
        # This is part of `self.plist`.
        self.flags = {}

    @classmethod
    def from_filebuffer(cls, filebuffer, **kwargs):
        """Return an emlx object from an emlx filebuffer."""

        bytecount = int(filebuffer.readline().strip())

        if kwargs.get("plist_only"):
            self = Emlx()
            filebuffer.seek(bytecount, 1)
        else:
            mime_bytes = filebuffer.read(bytecount)
            self = email.message_from_bytes(mime_bytes, _class=Emlx)
            self.headers = decode_headers(self)
            self.id = get_case_insensitive(self.headers, "Message-ID")
            self.url = self.id and f"message:{self.id}"

        self.bytecount = bytecount

        self.plist = plistlib.loads(filebuffer.read())
        self.flags_raw = self.plist.get("flags", 0)
        self.flags = decode_plist_flags(self.flags_raw)
        self.plist["flags"] = self.flags

        return self


def read(filepath_or_buffer, plist_only=False, **kwargs):
    """
    Read an emlx file into an `Emlx` object.

    Parameters
    ----------
    filepath_or_buffer : str or file-like object
        For example "12345.emlx" or objects with a `.read()` and `.seek()`
        method -- such as created by `open` or `io.BytesIO`.
    plist_only : bool, default False
        If `plist_only` is True, then the message MIME content will
        be skipped. The result will only include the `plist` attribute
        including `flags` and `bytecount`. This can speed things up.
    """
    if isinstance(filepath_or_buffer, str):
        filebuffer = open(filepath_or_buffer, "rb")
    elif is_file_like(filepath_or_buffer):
        filebuffer = filepath_or_buffer
    else:
        raise ValueError("`filepath_or_buffer` is not a str or file-like object.")

    try:
        kwargs["plist_only"] = plist_only
        result = Emlx.from_filebuffer(filebuffer, **kwargs)
    finally:
        filebuffer.close()

    return result


# Helper methods


def is_file_like(obj):
    """Is `obj` file-like?"""
    return hasattr(obj, "read") and hasattr(obj, "seek")


def decode_headers(message):
    """Decode headers in `email.message.Message`."""
    return {key: str(safe_decode_header(header)) for key, header in message.items()}


def safe_decode_header(header):
    """Not every email is RFC-conform."""
    try:
        return make_header(decode_header(header))
    except Exception:
        return header


def decode_plist_flags(integer):
    """Decode flags of emlx plist given by `integer`.

    See: https://www.jwz.org/blog/2005/07/emlx-flags/
    """
    result = {}
    integer |= 1 << 33
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
    # Fix for "attachment_count" sometimes set to 63. Why is this?
    attachment_count = result.get("attachment_count")
    if attachment_count == 63:
        del result["attachment_count"]
    return result


def get_case_insensitive(dictionary, key):
    """Get `key` in `dictionary` case-insensitively."""
    key = key.lower()
    return next(
        (value for other_key, value in dictionary.items() if other_key.lower() == key),
        None,
    )
