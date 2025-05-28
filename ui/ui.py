from ui.cli import CLI
class UI:
    def __init__(self, inventory, finance):
        self.inventory = inventory
        self.finance = finance
        self.suppliers = []
        self.current_order = None

    def run(self):
        cli = CLI(self)
        cli.cmdloop()