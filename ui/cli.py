import cmd

class CLI(cmd.Cmd):
    startmsg = "Welcome to WMS! Type help to list commands.\n"
    prompt = "User> "

    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.intro = self.startmsg
        self.prompt = self.prompt