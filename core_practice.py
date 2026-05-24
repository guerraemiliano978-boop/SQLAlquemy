from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, CheckConstraint, ForeignKey, insert, select, delete

engine = create_engine("sqlite:///practice.db")

metadata = MetaData()

minions = Table(
    "minions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False, unique=True),
    Column("num_eyes", Integer, CheckConstraint("num_eyes IN (1,2)")),
    Column("hairstyle", String)
)

weapons = Table(
    "weapons",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("hazard_level", Integer, CheckConstraint("hazard_level BETWEEN 1 AND 10"), nullable=False),
    Column("minion_id", Integer, ForeignKey(minions.c.id), nullable=False)
)

metadata.create_all(engine)

def minion_id(name):
    value = execute(select(minions.c.id).where(minions.c.name == name))
    return value.scalar()

def weapon_info():
    name = input("Weapon's name\n> ")
    while True:
        haz_lv = int(input("Weapon's hazard level? (Range between 1 and 10)\n> "))
        if haz_lv < 1 or haz_lv > 10:
            print("Invalid hazard level, try again.\n")
        else:
            assigned = input("Name of the assigned minion to the weapon\n> ")
            m_id = minion_id(assigned)
            data = [name, haz_lv, m_id]
            return data
        
def get_minion_name():
    name = input("Minion's name\n> ")
    return name

def get_weapon_name():
    name = input("Weapon's name\n> ")
    return name

def add_weapon(name, hazard_level, minion_id):
    execute(insert(weapons).values(name=name, hazard_level=hazard_level, minion_id=minion_id))

def execute(funct):
    with engine.begin() as conn:
        return conn.execute(funct)

def add_minion(name, eyes, hairstyle):
    execute(insert(minions).values(name=name, num_eyes=eyes, hairstyle=hairstyle))

def read_minion_weapon():
        result = execute(
            select(
                minions.c.name.label("minion_name"),
                weapons.c.name.label("weapon_name")
                ).join(weapons, minions.c.id == weapons.c.minion_id))
        for row in result:
            print(dict(row._mapping))

def read_by_minion(name):
        result = execute(
            select(
                minions.c.name.label("minion_name"),
                weapons.c.name.label("weapon_name"),
                weapons.c.hazard_level
                ).join(weapons, minions.c.id == weapons.c.minion_id).where(minions.c.name == name))
        for row in result:
            print(dict(row._mapping))


def read_by_weapon(name):
    result = execute(
        select(
        weapons.c.name.label("weapon_name"),
        weapons.c.hazard_level, 
        minions.c.name.label("minion_name")
        ).join(minions, weapons.c.minion_id == minions.c.id).where(weapons.c.name == name))
    for row in result:
            print(dict(row._mapping))


def minion_info():
    name = input("Minion's name\n> ")
    eyes = int(input("Number of eyes\n> "))
    hairstyle = input("Type of hairstyle\n> ")
    result = [name, eyes, hairstyle]
    return result

def ask_id():
    data = int(input("User's id\n> "))
    return data

def delete_weapon_and_minion(id):
    execute(
        delete(weapons).where(weapons.c.minion_id == id),
        delete(minions).where(minions.c.id == id)
        )

def add_menu():
    while True:
        choice = int(input("1 = minion\n2 = weapon\n> "))
        if choice not in (1,2):
            print("invalid option, try again\n")
        else:
            return choice
        
def read_menu():
    while True:
        choice = int(input("1 = All\n2 = Read by minion\n3 = Read by weapon\n> "))
        if choice not in (1,2,3):
             print("invalid option, try again\n")
        else:
            return choice


#MAIN
while True:
    choice = int(input("1 = Add\n2 = Read\n3 = Delete\n4 = exit\n> "))
    if choice == 1:
        add_choice = add_menu()
        if add_choice == 1:
            result = minion_info()
            add_minion(*result)
        else:
            result = weapon_info()
            add_weapon(*result)
    elif choice == 2:
        read_choice = read_menu()
        if read_choice == 1:
            read_minion_weapon()
        elif read_choice == 2:
            name = get_minion_name()
            read_by_minion(name)
        else:
            name = get_weapon_name()
            read_by_weapon(name)     
    elif choice == 3:
        name = get_minion_name()
        m_id = minion_id(name)
        delete_weapon_and_minion(m_id)
    else:
        break
