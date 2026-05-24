from sqlalchemy import create_engine, Table, Column, ForeignKey, String, Integer, MetaData, select

engine = create_engine()

metadata = MetaData()

customers = Table(
    "customers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String)
)

orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("order", String),
    Column("customer's_id", Integer, ForeignKey(customers.id))
)

#The customers table is the parent table and the orders table is the child one. The relationship is 
#in the foreignkey. When we want to relate them we use join. We can use
stmt = (
    select(customers.c.name, orders.c.order).join(orders, customers.c.id == orders.c.customer_id)
)