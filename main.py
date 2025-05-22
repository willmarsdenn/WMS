from core.inventory import Inventory
from core.finance import Finance
from ui import UI

def main():
    # Initialize core components
    inventory = Inventory()
    finance = Finance()
    
    # Set up UI (CLI or GUI)
    ui = UI(inventory, finance)
    
    # Start the application
    ui.run()

if __name__ == "__main__":
    main()