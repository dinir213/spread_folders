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
            cur.execute("DROP TABLE IF EXISTS '{subcategory}'".format(subcategory=subcategory[0]))
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
    return cur.execute("SELECT * FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchall()

async def add_position_db(subcategory_name, logins_parols, category_name):
    try:
        maxID = cur.execute("SELECT MAX(ID) FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchone()[0]
        maxID += 1
    except:
        maxID = 1
    result = []
    i = 0
    for login_parol in logins_parols:
        new_tuple = (maxID + i, login_parol[0], login_parol[1], login_parol[2])
        result.append(new_tuple)
        i += 1
    cur.executemany("INSERT INTO '{subcategory_name}' VALUES (?, ?, ?, ?)".format(subcategory_name=subcategory_name), result)
    db.commit()

async def del_position_db(subcategory_name, ID):
    if ID != 'all':
        cur.execute("DELETE FROM '{subcategory_name}' WHERE ID='{ID}'".format(subcategory_name=subcategory_name, ID=ID))
    else:
        cur.execute("DELETE FROM '{subcategory_name}'".format(subcategory_name=subcategory_name))
    db.commit()
async def sell_position_db(subcategory_name, count):
    minID = cur.execute("SELECT MIN(ID) FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchone()[0]
    result = ''
    # Выбираем все строки сразу, чтобы избежать повторных запросов в цикле
    rows = cur.execute(
        "SELECT * FROM '{subcategory_name}' WHERE ID >= ? LIMIT ?".format(subcategory_name=subcategory_name),
        (minID, count)).fetchall()
    # Если есть строки, обрабатываем их
    for i, row in enumerate(rows):
        result += f'{i + 1}. Login: {row[1]}, password: {row[2]}, рез. поле: {row[3]}\n'
    # Удаляем выбранные строки сразу в одном запросе
    cur.execute("DELETE FROM '{subcategory_name}' WHERE ID >= ? AND ID < ?".format(subcategory_name=subcategory_name), (minID, minID + len(rows)))
    # Коммитим изменения после выполнения всех операций
    db.commit()
    return result

async def update_count_tovs_db(value, tov_level, category_name, subcategory_name=''):
    if tov_level == 'category':
        tov_count = cur.execute("SELECT COUNT(*) FROM '{category_name}'".format(category_name=category_name)).fetchone()[0]
        cur.execute("UPDATE tov_categories SET tov_count=? WHERE category_name=?", (tov_count, category_name))
    elif tov_level == 'subcategory':
        tov_count = cur.execute("SELECT COUNT(*) FROM '{subcategory_name}'".format(subcategory_name=subcategory_name)).fetchone()[0]
        cur.execute("UPDATE '{category_name}' SET tov_count=? WHERE subcategory_name=?".format(category_name=category_name), (tov_count, subcategory_name))
    db.commit()
# Получение информации о конкретном товаре для его отображения клиентам
async def get_info_about_tov(category_name, subcategory_name):
    return cur.execute("SELECT * FROM '{category_name}' WHERE subcategory_name='{subcategory_name}'".format(category_name=category_name, subcategory_name=subcategory_name)).fetchall()[0]

# Реферальная система. Получение и изменение процента от рефераллов:
async def get_percent_referral_db():
    return float(cur.execute("SELECT percent_ref FROM percent_referral").fetchone()[0])/100
async def update_percent_referral_db(new_percent):
    cur.execute("DELETE FROM percent_referral")
    cur.execute("INSERT INTO percent_referral VALUES (?)", (new_percent,))
    db.commit()

# Режим работы бота. Включен для неадминов или выключен

async def get_work_mode_db():
    return int(open("work_bot.txt", "r").read())
async def update_work_mode_db(mode):
    with open('work_bot.txt', 'w') as f:
        f.write(str(mode))
