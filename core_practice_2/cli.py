from sales_register import Register
from inventory_management import InventoryManagement
from db import engine, ingredients, menu
from sqlalchemy import select

class CLI:
    def __init__(self, register: Register, inventory_management: InventoryManagement):
        self.register = register
        self.inv_man = inventory_management
    

    #GENERAL LOGIC
    def verify_input(self, funct):
        while True:
            try:
                return funct()
            except ValueError:
                print("\nInavalid value, please use a number\n")

    def boot_up(self):
        while True:    
            print("--- WELCOME TO THE KRUSTY KRAB POS ---\nPlease select an option\n")
            choice = int(input("1 = POS\n2 = Inventory management\n> "))
            if choice not in (1, 2):
                print("Invalid choice, please try again\n")
            else:
                return choice
            
    def main(self):
        while True:
            choice = self.boot_up()
            if choice == 1:
                self.register_engine()
            else:
                self.inventory_management_engine()
                pass
            
            cont = input("Do you want to exit the program? (y/n)\n> ").lower()
            if cont == "y":
                break


    #REGISTER LOGIC 
    def get_cx_name(self):
        print("\nWe will create a new ticket!\n")
        customer = input("Customer's name\n> ")
        return customer
    
    
    def get_items_list(self):
        with engine.connect() as conn:
            stmt = select(menu.c.id, menu.c.item)
            result = conn.execute(stmt)
            data = {}
            for row in result:
                data[row[0]] = row[1]

            i = len(data) 
            data[i + 1] = "Finish order"
            return data
        
 
    def get_item_id(self, items_list):
        while True:
            print("\nWhat does the customer want to order?\n")
            for k, v in items_list.items():
                print(f"{k} = {v}")

            choice = self.verify_input(lambda: int(input("> ")))
            if choice not in items_list:
                print("\nInvalid choice, please try again!\n")

            else:
                return choice
            

    def get_quantity(self):
        print("\nHow many does the customer want to order?\n")
        quantity = self.verify_input(lambda: int(input("Insert the amount\n> ")))
        return quantity


    def get_order(self):
        while True:
            items_list = self.get_items_list()
            item_id = self.get_item_id(items_list)
            if items_list[item_id] == "Finish order":
                return
            else:
                quantity = self.get_quantity()
                self.register.add_row(item_id, quantity)

              
    def get_order_receipt(self):
        receipt = self.register.get_receipt()
        total = self.register.calc_total(receipt)
        print("\n--- Receipt ---\n")
        for d in receipt:
            print(f"Product: {d["item"]} / Price: ${d["price"]}, / Quantity: {d["quantity"]}")
        print(f"\nTotal amount to pay: ${total:.2f}")
        return total
    
    
    def end_transaction(self, total, payment, cx_name):
        valid_transaction = self.register.validate_transaction(total, payment)
        if valid_transaction == True:
            change = self.register.calc_change(total, payment)
            print(f"The customer's exchange is ${change:.2f}")
            self.register.commit_order(cx_name)
            print("\nTell the customer to come back soon Squidward!!\n")
        else:
            print("\nNot enough money!! No krabby patties for this customer!")


    def new_order(self):
        self.register.clear_all()
        cx_name = self.get_cx_name()
        self.get_order()
        total = self.get_order_receipt()
        payment = self.verify_input(lambda: float(input("\nCustomer's payment amount\n> ")))
        self.end_transaction(total, payment, cx_name)

    def register_engine(self):
        while True:
                self.new_order()
                cont = input("\nDo you have another customer? (y/n)\n> ")
                if cont == "n":
                    break


   
    #INVENTORY MANAGEMENT LOGIC
    def get_ingredients_list(self):
        with engine.connect() as conn:
            stmt = select(ingredients.c.id, ingredients.c.ingredient)
            result = conn.execute(stmt)
            data = {}
            for row in result:
                data[row[0]] = row[1]

            return data
    
    def stock_data(self, data):
        print("\n--- List of ingredients ---\n")
        for k, v in data.items():
            print(f"{k} = {v}")
        
        chosen_id = int(input("\nSelect the ingredient\n> "))
        added_amount = int(input(f"\nHow many items will be added to the {data[chosen_id]} stock?\n> "))
        return (chosen_id, added_amount)
    
    def read_ingredients_table(self):       
        with engine.connect() as conn:
            stmt = select(ingredients)
            result = conn.execute(stmt)
            for row in result:
                print(dict(row._mapping))
    
    def inventory_management_engine(self):
        while True:
            data = self.get_ingredients_list()
            values = self.stock_data(data)
            self.inv_man.add_stock(values)
            print("\n--- Here are the new values! ---\n")
            self.read_ingredients_table()

            cont = input("\nDo you want to continue using the inventory management? (y/n)\n> ")
            if cont == "n":
                break




#MAIN CODE
inventory_management = InventoryManagement()
register = Register(inventory_management)
cli = CLI(register, inventory_management)
cli.main()



        

