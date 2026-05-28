from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table, Float, ForeignKey, insert, select, update

engine = create_engine("sqlite:///database.db")

metadata = MetaData()

menu = Table(
    "menu",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("item", String, nullable=False),
    Column("price", Float, nullable=False)
)

ingredients = Table(
    "ingredients",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ingredient", String, nullable=False),
    Column("stock", Integer, nullable=False)
)

recipe = Table(
    "recipe",
    metadata,
    Column("item_id", Integer, ForeignKey(menu.c.id), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey(ingredients.c.id), primary_key=True),
    Column("quantity", Integer, nullable=False)
)

ticket = Table(
    "ticket",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("customer_name", String, nullable=False)
)

ticket_items = Table(
    "ticket_items",
    metadata,
    Column("ticket_id", Integer, ForeignKey(ticket.c.id), primary_key=True),
    Column("item_id", Integer, ForeignKey(menu.c.id), primary_key=True),
    Column("quantity", Integer, nullable=False),
)


metadata.create_all(engine)

def execute(stmt):
    with engine.begin() as conn:
        return conn.execute(stmt)
    
def get_item_id(name):
    result = execute(select(menu.c.id).where(menu.c.item == name))
    return result.scalar()

def get_ingredient_id(name):
    result = execute(select(ingredients.c.id).where(ingredients.c.ingredient == name))
    return result.scalar()




