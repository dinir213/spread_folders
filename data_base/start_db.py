from create_bot import db, cur

def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, username TEXT, balance REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS menu_payment(msg_id TEXT PRIMARY KEY, value_amount TEXT, user_id TEXT, payment_id_or_uuid TEXT, sign TEXT, order_id TEXT, paym_method TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS payment_methods(payment_name TEXT PRIMARY KEY, payment_callbackdata TEXT, work_mode TEXT)")
    payment_methods = [('yookassa', 'getcheck_yookassa', '1'),
                       ('cryptomus', 'getcheck_cryptomus', '1')]
    if cur.execute("SELECT * FROM payment_methods").fetchall() == []:
        cur.executemany("INSERT INTO payment_methods (payment_name, payment_callbackdata, work_mode) VALUES (?, ?, ?)", payment_methods)
    cur.execute("CREATE TABLE IF NOT EXISTS tov_categories(category_name TEXT PRIMARY KEY, tov_count TEXT)")
    db.commit()
