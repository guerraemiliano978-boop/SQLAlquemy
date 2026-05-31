from db import engine, ticket, ticket_items, ingredients
from sqlalchemy import select


ticket_stmt = select(ticket)
ticket_items_stmt = select(ticket_items)
ingredients_stmt = select(ingredients)

with engine.connect() as conn:
    result = conn.execute(ticket_stmt)
    for row in result:
        print(dict(row._mapping))

with engine.connect() as conn:
    result = conn.execute(ticket_items_stmt)
    for row in result:
        print(dict(row._mapping))

with engine.connect() as conn:
    result = conn.execute(ingredients_stmt)
    for row in result:
        print(dict(row._mapping))




