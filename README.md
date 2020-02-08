Emlx
=====

Emlx is a lightweight parser for `.emlx` files as used by Mail.app.


Install
-------

Install and update using `pip`:

```
pip install emlx
```


Example
-------

```pycon
>>> import emlx
>>> message = emlx.read("12345.emlx")
>>> message.bytecount
1781
>>> message.data["Message-Id"]
'<07F45222-4A09-11EA-BBA5-5CF9389AFA5E@example.com>'
>>> message.data.keys()
['From', 'Mime-Version', 'Content-Type', 'Subject', 'Date', ...]
>>> message.plist
{'date-received': 1581123200, 'flags': {'read': True, ...}, ...}
```


History
-------

The `emlx` file format was introduced by Apple in 2005. It is similar to `eml`-files with an added bytecount (start) and plist (end). For more, see https://en.wikipedia.org/wiki/Email#Filename_extensions
