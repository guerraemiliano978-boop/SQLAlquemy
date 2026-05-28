from sales_register import Register

class CLI:
    def __init__(self, register: Register):
        self.register = register
        self.current_items_quantity = {}
        self.items_list = {
            1: "krabby patty",
            2: "double krabby patty",
            3: "kelp shake",
            4: "kelp fries"
        }

    def create_ticket(self):
        print("\nWe will create a new ticket!\n")
        customer = input("Customer's name\n> ")
        return self.register.create_ticket(customer)
    
    def get_items_quantity(self):
        print("\nWhat does the customer wants to order?\n")
        choice = int(input("1 = krabby patty\n2 = double krabby patty\n3 = kelp shake\n4 = kelp fries\n> "))
        item = self.items_list.get(choice)
        print("\nHow many does the customer wants to order?\n")
        quantity = int(input("Insert the amount\n> "))
        return (item, quantity)
    
    def insert_row(self, data: tuple):
        register.parse_item_quantity(data)
        return self.register.add_ticket_item_row()
    
    def get_order_price(self):
        order = self.register.get_ticket_items_list()
        #total = self.register.calc_total()
        for d in order:
            print(d)
        #print(f"Total: ${total}")
        #return total
    
    def return_change(self, total, payment):
        change = self.register.calc_change(total, payment)
        print(f"The customer exchange is ${change}")

    def new_order(self):
        self.register.clear_all()
        self.create_ticket()
        while True:
            data = self.get_items_quantity()
            self.insert_row(data)
            cont = input("\nIs the order already complete? (y/n)\n> ").lower()
            if cont == "y":
                break
        total = self.get_order_price()
        payment = float(input("\nCustomer's payment amount\n> "))
        #self.return_change(total, payment)

        print("\nTell the customer to come back soon Squidward!!\n")

    def main(self):
        while True:
            self.new_order()
            cont = input("\nDo you have another customer? (y/n)\n> ")
            if cont == "n":
                break



register = Register()
cli = CLI(register)
cli.main()



        

