from sales_register import Register
from inventory_managment import InventoryManagement

class CLI:
    def __init__(self, register: Register):
        self.register = register
        self.items_list = {
            1: "krabby patty",
            2: "double krabby patty",
            3: "kelp shake",
            4: "kelp fries"
        }
    
    def verify_input(self, funct):
        while True:
            try:
                return funct()
            except ValueError:
                print("\nInavalid value, please use a number\n")

    def get_cx_name(self):
        print("\nWe will create a new ticket!\n")
        customer = input("Customer's name\n> ")
        return customer
    
    def get_item_quantity(self):
        while True:
            print("\nWhat does the customer want to order?\n")
            choice = self.verify_input(lambda: int(input("1 = krabby patty\n2 = double krabby patty\n3 = kelp shake\n4 = kelp fries\n> ")))
            if choice not in (1,2,3,4):
                print("\nInvalid choice, please try again!\n")
            else:
                break    
        item = self.items_list.get(choice)
        print("\nHow many does the customer want to order?\n")
        quantity = self.verify_input(lambda: int(input("Insert the amount\n> ")))
        return (item, quantity)
    
    def send_row(self, data: tuple):
        return self.register.add_row(data)
    
    def get_order(self):
        while True:
            data = self.get_item_quantity()
            self.send_row(data)
            cont = input("\nIs the order already complete? (y/n)\n> ").lower()
            if cont == "y":
                break
    
    def get_order_receipt(self):
        receipt = self.register.get_receipt()
        total = self.register.calc_total(receipt)
        for d in receipt:
            print(d)
        print(f"Total: ${total:.2f}")
        return total
    
    def end_transaction(self, total, payment, cx_name):
        valid_transaction = self.register.validate_transaction(total, payment)
        if valid_transaction == True:
            change = self.register.calc_change(total, payment)
            print(f"The customer's exchange is ${change:.2f}")
            self.commit_order(cx_name)
            print("\nTell the customer to come back soon Squidward!!\n")
        else:
            print("\nNot enough money!! No krabby patties for this customer!")

    def commit_order(self, cx_name):
        self.register.commit_order(cx_name)

    def new_order(self):
        self.register.clear_all()
        cx_name = self.get_cx_name()
        self.get_order()
        total = self.get_order_receipt()
        payment = self.verify_input(lambda: float(input("\nCustomer's payment amount\n> ")))
        self.end_transaction(total, payment, cx_name)

    def main(self):
        while True:
            self.new_order()
            cont = input("\nDo you have another customer? (y/n)\n> ")
            if cont == "n":
                break



inventory_management = InventoryManagement()
register = Register(inventory_management)
cli = CLI(register)
cli.main()



        

