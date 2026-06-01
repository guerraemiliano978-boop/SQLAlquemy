from db import engine, recipe, ingredients
from sqlalchemy import select, update


class InventoryManagement:
    def __init__(self):
        self.current_changes = {}

        
    def validate_order_stock(self, order):
        self.current_changes.clear()
        valid_order = True
        for row in order:
            item_id = row.get("item_id")
            order_quantity = row.get("quantity")
            recipe_rows = self.get_recipe(item_id)
            valid_order = self.verify_stock(recipe_rows, order_quantity)
            if valid_order == False:
                return False
            
        return True
      
    def get_recipe(self, item_id):
        with engine.connect() as conn:
            stmt = select(
                    recipe.c.ingredient_id,
                    recipe.c.quantity
                    ).where(recipe.c.item_id == item_id)
            return conn.execute(stmt)
    
    def verify_stock(self, recipe_rows, order_quantity):
        with engine.connect() as conn:
            for row in recipe_rows:
                result = conn.execute(select(ingredients.c.stock).where(ingredients.c.id == row[0]))
                stock = result.scalar()
                previous_amount = self.current_changes.get(row[0], 0)
                total_amount = previous_amount + row[1]*order_quantity
                if total_amount > stock:
                    return False
                else:
                    self.current_changes[row[0]] = total_amount

            return True
        
    def commit_changes(self):
        with engine.begin() as conn:
            for ingredient_id, amount in self.current_changes.items():
                conn.execute(
                    update(ingredients).where(
                        ingredients.c.id == ingredient_id).values(stock=ingredients.c.stock - amount))
    
    def add_stock(self, data):
        with engine.begin() as conn:
            stmt = update(ingredients).where(ingredients.c.id == data[0]).values(stock=ingredients.c.stock + data[1])
            conn.execute(stmt)





        
        
                

                
                    

        





    
