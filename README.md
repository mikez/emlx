Emlx
=====

Emlx is the lightweight parser for `.emlx` files as used by Mail.app.


Install
-------

Install and update using `pip`:

```
pip install emlx
```


Basic usage
-----------

```pycon
>>> import emlx
>>> m = emlx.read("12345.emlx")
>>> m.headers
{'Subject': 'Re: Emlx library ✉️',
 'From': 'Michael <michael@example.com>',
 'Date': 'Thu, 30 Jan 2020 20:25:43 +0100',
 'Content-Type': 'text/plain; charset=utf-8',
 ...}
>>> m.headers['Subject']
'Re: Emlx library ✉️'
>>> m.plist
{'color': '000000',
 'conversation-id': 12345,
 'date-last-viewed': 1580423184,
 'flags': {...}
 ...}
>>> m.flags
{'read': True, 'answered': True, 'attachment_count': 2}
```


Architecture
------------

An `.emlx` file consists of three parts:

1. bytecount on first line;
2. email content in MIME format (headers, body, attachments);
3. Apple property list (plist) with metadata.

The second part (2.) is parsed by the `email` library. It is included in the Python standard library. Message objects generated by `emlx` extend `email.message.Message` and thus give access to its handy features. Additionally, `emlx` message objects provide the attributes `bytecount` (1.) as integer and `plist` (3.) as a Python dictionary. For convenience, it also offers the attributes `headers`, `url`, `id`, and `flags`.


History
-------

The `emlx` file format was introduced by Apple in 2005. It is similar to `eml`-files popular with other email clients; the difference is the added bytecount (start) and plist (end). For more, see [here](https://en.wikipedia.org/wiki/Email#Filename_extensions).
