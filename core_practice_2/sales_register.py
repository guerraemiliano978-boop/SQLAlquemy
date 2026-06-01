from db import menu, ticket, ticket_items, engine
from inventory_management import InventoryManagement
from sqlalchemy import insert, select



class Register:
    def __init__(self, inventory_managment: InventoryManagement):
        self.inventory_managment = inventory_managment
        self.current_order = []
   

    def clear_all(self):
        self.current_order.clear()

    def add_row(self, item_id, quantity):
        row = {
           "item_id": item_id,
           "quantity": quantity 
        }
        self.current_order.append(row)
             
    def get_item_price(self, item_id):
        with engine.connect() as conn:
            stmt = select(menu.c.item, menu.c.price).where(menu.c.id == item_id)
            result = conn.execute(stmt)
            return result.fetchone()    
        
    def get_receipt(self):
        current_receipt = []
        for row in self.current_order:
            quantity = row.get("quantity")
            item_id = row.get("item_id")
            data = self.get_item_price(item_id)
            receipt_row = {
            "item": data[0],
            "price": data[1],
            "quantity": quantity
            }
            current_receipt.append(receipt_row)
        
        return current_receipt
    
    def calc_total(self, current_receipt):
        total = 0
        for d in current_receipt:
            price = d.get("price")
            quantity = d.get("quantity")
            total += price*quantity
        return total
    
    def validate_transaction(self, total, payment):
        enough_stock = self.inventory_managment.validate_order_stock(self.current_order)

        if payment >= total and enough_stock == True:
             return True
        else:
             return False
   
    def calc_change(self, total, payment):
        result = payment - total
        return result
    
    def create_ticket(self, cx_name):
        with engine.begin() as conn:
            stmt = insert(ticket).values(customer_name=cx_name)
            result = conn.execute(stmt)
            return result.inserted_primary_key[0]
           
    def commit_order(self, cx_name):
        ticket_id = self.create_ticket(cx_name)
        final_order = []
        for row in self.current_order:
            final_row = {
                "ticket_id": ticket_id,
                "item_id": row.get("item_id"),
                "quantity": row.get("quantity")
                }
            final_order.append(final_row)

        with engine.begin() as conn:
            stmt = insert(ticket_items).values(final_order)
            conn.execute(stmt)

        self.inventory_managment.commit_changes()


            



        




