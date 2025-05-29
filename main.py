from core.inventory import Inventory
from core.finance import Finance
from ui.ui import UI

def main():
    inventory = Inventory()
    finance = Finance()
    
    ui = UI(inventory, finance)
    ui.run()

if __name__ == "__main__":
    main()