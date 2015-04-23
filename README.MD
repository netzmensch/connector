#Connector

![image](http://i.imgur.com/rXttICG.png?1)

This Python Tool shows you a menu list of your ssh servers. If you choose a server and press enter, Connector will open a new iTerm Tab and run ssh [Server].

Optionally, you can toggle the tunnel mode. If activated, Connector will run an ssh connect via the configured tunnel server.(ssh -A -t [Tunnel Server] ssh [Server])

###Requirements

urwid ([http://urwid.org](http://urwid.org))

`pip install urwid`

osascript ([https://pypi.python.org/pypi/osascript/0.0.4](https://pypi.python.org/pypi/osascript/0.0.4))

`pip install osascript`