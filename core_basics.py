#Those are the main tools we need to work with core
from sqlalchemy import create_engine, MetaData, String, Table, Integer, Column, insert, select, update, delete

#We create the engine with the database we want to work with. It can be whatever type of SQL databse
#it handles the translation automatically. For this example I would use sqlite
engine = create_engine("sqlite:///practice.db")

#We create an instance of MetaData
metadata = MetaData()

#And then we proceed to create an instance of a Table object
#The order of arguments is 'name', 'metadata' and 'columns'. Refer to the example if needed
users = Table (
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("age", Integer),
    Column("role", String)
)


#This is a basic table for users. AS you can see we can set up the data type, we can select it as the
#primary key and choose if the column can't be empty. 

#This ones creates all the tables stored inside metadata en creates them. As we can remember, we added
#metadata inside the users Table, so it will create it inside engine, our database
metadata.create_all(engine)

#CRUD OPERATIONS
#First, we need to activate the connection
conn = engine.connect()
#The first actin is to create, we use insert
statement = users.insert()
parameters = [{"name": "Bob", "age": 25, "role": "user"}, {"name": "Stuart", "age": 30, "role": "agent"}]
conn.execute(statement, parameters)
#The function execute excpects stmnt, prmtrs. We can set it up like this

#We can also use the .values() function to pass a single statement and it works too.
statement = users.insert().values([{"name": "Kevin", "age": 35, "role": "agent"}])
conn.execute(statement)
    
#For 'read' we use select and then we can print it if need
statement = users.select()
result = conn.execute(statement)
for row in result:
    print(row)

#Now we can introduce a filter, a tool we use to choose some elements inside a table. We use WHERE
#An example using the previous command would be:
statement = users.select().where(users.c.age > 25)
result = conn.execute(statement)
for row in result:
    print(row)
#As we can see, in the example we have, using the filter we only get two users. 

#Now we can introduce 'update'. We use .update()
statement = users.update().where(users.c.name == "Kevin").values(role="admin")
conn.execute(statement)

#The last action is 'delete'. For it we use .delete()
statement = users.delete().where(users.c.name == "Bob")
conn.execute(statement)

statement = users.select()
result = conn.execute(statement)
for row in result:
    print(row)

#Remember that if you want to persist information, you must commit it
conn.commit()

#Now, we can use the previous CRUD operators, but they are the legacy way of doing so. The new standard
#is to use the functions imported from the library like this
insert(users)
select(users)
update(users)
delete(users)
#There are many technicals reasons to choose the latest method, but it's also great because it 
#bridges the core with the ORM way of doing it. 

#Finally, we discussed about the need to commit each change. There is another, preferred way of handle
#it. We use conn as engine.begin() instead of engine.connect(). It has a couple of great perks. For
#instance, it handles the errors, if any, for you. If there isn't any errors in the operations, it 
#commits the information for you. Usually engine.begin() is the preferred way.
with engine.begin() as conn:
    conn.execute()