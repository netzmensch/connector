#!/usr/bin/env python
import urwid
import osascript
import yaml
import argparse


class Connector():
    def __init__(self, settingsPath):
        self.defaultHeadline = "Connector 1.0 - tunnel mode (press t): "
        self.tunnelMode = False
        settings = self.loadSettings(settingsPath)
        self.tunnelServer = settings['tunnelServer']
        self.items = []
        self.terminal = settings['terminal']
        self.server = settings['servers']

        self.palette = [
            ('body', 'dark green', '', 'standout'),
            ('focus', 'dark red', '', 'standout'),
            ('head', 'black', 'light gray')
        ]

        server_keys = sorted(self.server.keys())

        for serverId in server_keys:
            self.items.append(ItemWidget(serverId, self.server[serverId]))

        header = urwid.AttrMap(urwid.Text(self.defaultHeadline + "disabled"), 'head')
        self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.items))
        self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'), header=header)

    def main(self):
        loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.keystroke)
        loop.run()

    def loadSettings(self, fileName):
        yamlContent = self.getFileContent(fileName)

        return yaml.load(yamlContent)

    def getFileContent(self, fileName):
        with file(fileName) as f:
            s = f.read()
        return s

    def keystroke(self, input):
        if input in ('q', 'Q'):
            raise urwid.ExitMainLoop()

        if input in ('t', 'T'):
            if self.tunnelMode is True:
                self.setHeaderText(self.defaultHeadline + "disabled")
                self.tunnelMode = False
            else:
                self.setHeaderText(self.defaultHeadline + "active, use " + self.tunnelServer + " as tunnel")
                self.tunnelMode = True

        if input is 'enter':
            target = self.listbox.get_focus()[0].content
            sshCommand = "ssh "

            if self.tunnelMode is True:
                 sshCommand += "-A -t " + self.tunnelServer + " ssh "

            sshCommand += target

            self.runItermCommand(sshCommand)

    def setHeaderText(self, headerText):
        self.view.set_header(urwid.AttrMap(urwid.Text(headerText), 'head'))

    def runItermCommand(self, sshCommand):
        commandTerminal = """
        tell application "Terminal"
            activate
            tell application "System Events"
                tell process "Terminal" to keystroke "t" using command down
            end
            do script "%SSH_COMMAND%" in front window
        end tell
        """
        commandIterm = """
        tell application "iTerm"
            tell current terminal
                launch session "Default Session"
                tell the last session
                    write text "%SSH_COMMAND%"
                end tell
            end tell
        end tell
        """

        if self.terminal == "iterm":
            command = commandIterm
        else:
            command = commandTerminal

        command = command.replace('%SSH_COMMAND%', sshCommand)
        osascript.osascript(command)



class ItemWidget (urwid.WidgetWrap):
    def __init__ (self, id, description):
        self.id = id
        self.content = description
        self.item = [
            ('fixed', 40, urwid.Padding(urwid.AttrWrap(
                urwid.Text('%s:' % id), 'body', 'focus'), left=2)),
            urwid.AttrWrap(urwid.Text('%s' % description), 'body', 'focus'),
        ]
        w = urwid.Columns(self.item)
        self.__super.__init__(w)

    def selectable (self):
        return True

    def keypress(self, size, key):
        return key


if __name__ == '__main__':
    settingsPath = "config.yml"
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', help='alternative path to config file (default: config.yml)')
    args = parser.parse_args()

    if args.config:
        settingsPath = args.config

    app = Connector(settingsPath)
    app.main()