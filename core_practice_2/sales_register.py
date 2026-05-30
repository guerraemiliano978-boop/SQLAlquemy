from db import menu, ticket, ticket_items, engine
from sqlalchemy import insert, select


class Register:
    def __init__(self):
        self.current_ticket_id = None
        self.current_item_name = None
        self.current_item_id = None
        self.current_quantity = None
        self.current_order = []
        self.current_receipt_order = []
    
    def clear_all(self):
        self.clear_row()
        self.current_ticket_id = None
        self.current_order.clear()
        self.current_receipt_order.clear()

    def clear_row(self):
        self.current_item_id = None
        self.current_item_name = None
        self.current_quantity = None
    
    def create_ticket(self, cx_name):
        with engine.begin() as conn:
            stmt = insert(ticket).values(customer_name=cx_name)
            result = conn.execute(stmt)
            self.current_ticket_id = result.inserted_primary_key[0]
            #print(f"for debbuging, ticket id {self.current_ticket_id}")
            return self.current_ticket_id

    def parse_item_quantity(self, data: tuple):
        self.current_item_name = data[0]
        self.get_item_id()
        self.current_quantity = data[1]
    
    def get_item_id(self):
        with engine.connect() as conn:
            stmt = select(menu.c.id).where(menu.c.item == self.current_item_name)
            result = conn.execute(stmt)
            self.current_item_id = result.scalar()

    def add_ticket_item_row(self):
        row = {
           "ticket_id": self.current_ticket_id,
           "item_id": self.current_item_id,
           "quantity": self.current_quantity 
        }
        self.current_order.append(row)
        
        #with engine.begin() as conn:
            #stmt = insert(
                #ticket_items
                #).values(ticket_id=self.current_ticket_id, 
                         #item_id=self.current_item_id, 
                         #quantity=self.current_quantity)
            #result = conn.execute(stmt)
            #self.clear_row()
            #return result
    
    def get_ticket_items_list(self):
        self.current_receipt_order.clear()
        receipt_row = {}
        for row in self.current_order:
            quantity = row.get("quantity")
            item_id = row.get("item_id")
            data = self.get_item_price(item_id)
            receipt_row = {
            "item": data[0],
            "price": data[1],
            "quantity": quantity
            }
            self.current_receipt_order.append(receipt_row)
        
        return self.current_receipt_order

    def get_item_price(self, item_id):
        with engine.connect() as conn:
            stmt = select(menu.c.item, menu.c.price).where(menu.c.id == item_id)
            result = conn.execute(stmt)
            return result.fetchone()        

        #with engine.connect() as conn:
            #stmt = select(menu.c.item, 
                          #menu.c.price,
                          #ticket_items.c.quantity
                          #).select_from(
                              #ticket_items.join(
                                  #menu, ticket_items.c.item_id == menu.c.id)).where(
                                      #ticket_items.c.ticket_id == self.current_ticket_id
                                  #)
            #result = conn.execute(stmt)
            #self.current_order = [dict(row._mapping) for row in result]
            #return self.current_order
        
    def calc_total(self):
        total = 0
        for d in self.current_receipt_order:
            price = d.get("price")
            quantity = d.get("quantity")
            total += price*quantity
        return total
    
    def validate_transaction(self, total, payment):
        if total > payment:
             return False
        else:
             return True
   
    def calc_change(self, total, payment):
        result = payment - total
        return result

    def commit_order(self):
        with engine.begin() as conn:
            stmt = insert(ticket_items).values(self.current_order)
            conn.execute(stmt)


            



        




