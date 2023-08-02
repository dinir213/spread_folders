from create_bot import db, cur

# Работа с БД, содержащей информацию о способах оплаты:
async def view_all_payment_methods():
    return cur.execute("SELECT * FROM payment_methods")
async def turn_payment_method_db(work_mode, payment_name):
    cur.execute(f"UPDATE payment_methods SET work_mode={work_mode} WHERE payment_name='{payment_name}'")
    db.commit()

# Работа с БД, содержащей информацию о категориях, подкатегориях и позициях товаров:
async def view_all_categories_db():
    return cur.execute("SELECT category_name FROM tov_categories").fetchall()

async def add_category_db(category_name):
    cur.execute("INSERT INTO tov_categories VALUES (?, ?)", (category_name, '0'))
    cur.execute(f"CREATE TABLE IF NOT EXISTS {category_name}(subcategory_name TEXT PRIMARY KEY, tov_count TEXT, price REAL, description TEXT)")
    db.commit()
async def del_category_db(category_name):
    cur.execute(f"DELETE FROM tov_categories WHERE category_name='{category_name}'")
    subcategories_tables = cur.execute(f"SELECT subcategory_name FROM {category_name}").fetchall()
    if subcategories_tables != []:
        for subcategory in subcategories_tables:
            cur.execute(f"DROP TABLE IF EXISTS {subcategory[0]}")
            print(f'Удалена подкатегория {subcategory[0]} в категории {category_name}')
    cur.execute(f"DROP TABLE IF EXISTS {category_name}")
    db.commit()
async def view_all_subcategories_db(category_name):
    # print(cur.execute(f"SELECT * FROM {category_name}").fetchall())
    return cur.execute(f"SELECT subcategory_name FROM {category_name}").fetchall()

async def add_subcategory_db(category_name, subcategory_name, price, description):
    cur.execute(f"INSERT INTO {category_name} VALUES (?, ?, ?, ?)", (subcategory_name, '0', price, description))
    cur.execute(f"CREATE TABLE IF NOT EXISTS {subcategory_name}(ID INTEGER PRIMARY KEY, key1 TEXT, key2 TEXT, key3 TEXT)")
    db.commit()
async def del_subcategory_db(category_name, subcategory_name):
    print(category_name,type(category_name), subcategory_name, type(subcategory_name))
    cur.execute(f"DELETE FROM '{category_name}' WHERE subcategory_name='{subcategory_name}'")
    cur.execute(f"DROP TABLE IF EXISTS {subcategory_name}")
    db.commit()


async def view_all_position_db(subcategory_name):
    # print(f'Из таблицы категории товара {subcategory_name} хочу взять значение {cur.execute(f"SELECT key1 FROM {subcategory_name}").fetchall()}')
    return cur.execute(f"SELECT key1 FROM {subcategory_name}").fetchall()
async def add_position_db(subcategory_name, tov_position0, tov_position1, tov_position2, category_name):
    try:
        maxID = cur.execute(f"SELECT MAX(ID) FROM {subcategory_name}").fetchone()[0]
        maxID = maxID + 1
    except:
        maxID = 1
    cur.execute(f"INSERT INTO {subcategory_name} VALUES (?, ?, ?, ?)", (maxID, tov_position0, tov_position1, tov_position2))
    maxID_category_table = int(cur.execute(f"SELECT tov_count FROM {category_name}").fetchall()[0][0])
    print('maxid=', maxID_category_table)
    cur.execute(f"UPDATE {category_name} SET tov_count='{maxID_category_table + 1}' WHERE subcategory_name='{subcategory_name}'")
    db.commit()
async def del_position_db(subcategory_name, ID):
    print(ID,type(ID), subcategory_name, type(subcategory_name))

    print(f'subcategory_name = {subcategory_name},   ID = {ID}')
    cur.execute(f"DELETE FROM {subcategory_name} WHERE ID='{ID}'")
    # cur.execute(f"DROP TABLE IF EXISTS {subcategory_name}")
    db.commit()