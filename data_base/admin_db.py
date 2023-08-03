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
    cur.execute(f"CREATE TABLE IF NOT EXISTS [{category_name}] (subcategory_name TEXT PRIMARY KEY, tov_count TEXT, price REAL, description TEXT, img_code TEXT)")
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
    return cur.execute(f"SELECT subcategory_name FROM [{category_name}]").fetchall()

async def add_subcategory_db(category_name, subcategory_name, price, description, img_code):
    cur.execute("INSERT INTO '{category_name}' VALUES (?, ?, ?, ?, ?)".format(category_name=category_name), (subcategory_name, '0', price, description, img_code))
    cur.execute(f"CREATE TABLE IF NOT EXISTS [{subcategory_name}] (ID INTEGER PRIMARY KEY, key1 TEXT, key2 TEXT, key3 TEXT)")
    await update_count_tovs_db(+1, 'category', category_name, subcategory_name)
    db.commit()
async def del_subcategory_db(category_name, subcategory_name):
    cur.execute("DELETE FROM '{category_name}' WHERE subcategory_name='{subcategory_name}'".format(category_name=category_name, subcategory_name=subcategory_name))
    cur.execute(f"DROP TABLE IF EXISTS [{subcategory_name}]")
    db.commit()


async def view_all_position_db(subcategory_name):
    # print(f'Из таблицы категории товара {subcategory_name} хочу взять значение {cur.execute(f"SELECT key1 FROM {subcategory_name}").fetchall()}')
    return cur.execute(f"SELECT * FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchall()

async def add_position_db(subcategory_name, tov_position0, tov_position1, tov_position2, category_name):
    try:
        maxID = cur.execute("SELECT MAX(ID) FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchone()[0]
        maxID = maxID + 1
    except:
        maxID = 1
    cur.execute("INSERT INTO '{subcategory_name}' VALUES (?, ?, ?, ?)".format(subcategory_name=subcategory_name), (maxID, tov_position0, tov_position1, tov_position2))
    db.commit()

async def del_position_db(subcategory_name, ID):
    if ID != 'all':
        cur.execute("DELETE FROM '{subcategory_name}' WHERE ID='{ID}'".format(subcategory_name=subcategory_name, ID=ID))
    else:
        cur.execute("DELETE FROM '{subcategory_name}'".format(subcategory_name=subcategory_name))
    db.commit()
async def update_count_tovs_db(value, tov_level, category_name, subcategory_name=''):
    if tov_level == 'category':
        tov_count = len(cur.execute("SELECT * FROM '{category_name}'".format(category_name=category_name)).fetchall())
        cur.execute("UPDATE tov_categories SET tov_count='{tov_count}' WHERE category_name='{category_name}'".format(tov_count=tov_count, category_name=category_name))
    elif tov_level == 'subcategory':
        if value == 'all':
            tov_count = 0
        else:
            tov_count = len(cur.execute("SELECT * FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchall())
            tov_count = str(tov_count)
        cur.execute("UPDATE '{category_name}' SET tov_count='{tov_count}' WHERE subcategory_name='{subcategory_name}'".format(category_name=category_name, tov_count=tov_count, subcategory_name=subcategory_name))

    db.commit()