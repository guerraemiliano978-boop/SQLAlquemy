from db import menu, ingredients, recipe, execute, get_ingredient_id, get_item_id
from sqlalchemy import select, insert


items_list =  [
        {"item": "krabby patty" , "price":3.99},
        {"item": "double krabby patty" , "price":4.50},
        {"item": "kelp shake" , "price":2.50},
        {"item": "kelp fries" , "price":2.25},
    ]

ingredients_list =  [
        {"ingredient": "krabby patty meat" , "stock":100},
        {"ingredient": "seaweed buns" , "stock":100},
        {"ingredient": "cheese" , "stock":50},
        {"ingredient": "kelp strips" , "stock":80},
        {"ingredient": "kelp juice" , "stock":75}
    ]

execute(insert(menu).values(items_list))
  
execute(insert(ingredients).values(ingredients_list))


recipe_list = [
    {"item_id": get_item_id("krabby patty"), 
     "ingredient_id": get_ingredient_id("krabby patty meat"), 
     "quantity": 1},
     {"item_id": get_item_id("krabby patty"), 
     "ingredient_id": get_ingredient_id("seaweed buns"), 
     "quantity": 1},
     {"item_id": get_item_id("krabby patty"), 
     "ingredient_id": get_ingredient_id("cheese"), 
     "quantity": 1},
     {"item_id": get_item_id("double krabby patty"), 
     "ingredient_id": get_ingredient_id("krabby patty meat"), 
     "quantity": 2},
     {"item_id": get_item_id("double krabby patty"), 
     "ingredient_id": get_ingredient_id("seaweed buns"), 
     "quantity": 1},
     {"item_id": get_item_id("double krabby patty"), 
     "ingredient_id": get_ingredient_id("cheese"), 
     "quantity": 2},
     {"item_id": get_item_id("kelp shake"), 
     "ingredient_id": get_ingredient_id("kelp juice"), 
     "quantity": 1},
     {"item_id": get_item_id("kelp fries"), 
     "ingredient_id": get_ingredient_id("kelp strips"), 
     "quantity": 6}
]


execute(insert(recipe).values(recipe_list))
   


menu_stmt = select(menu)

ingredients_stmt =select(ingredients)

recipe_stmt = select(recipe)

recipe_with_names_stmt = select(
    menu.c.item, ingredients.c.ingredient, recipe.c.quantity
    ).select_from(recipe.join(menu, recipe.c.item_id == menu.c.id
                              ).join(ingredients, recipe.c.ingredient_id == ingredients.c.id)
                              )
                  
result = execute(recipe_with_names_stmt)
for row in result:
    print(dict(row._mapping))
