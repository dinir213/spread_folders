from create_bot import db, cur

async def input_value_amount_in_menu_payment(call):
    cur.execute(f"INSERT OR REPLACE INTO menu_payment VALUES(?, ?, ?, ?, ?, ?, ?)", (call.message.message_id, '', call.from_user.id, '', '', '', ''))
    db.commit()

async def get_value_amount_in_menu_payment(call):
    return cur.execute("SELECT value_amount FROM menu_payment WHERE msg_id == '{key}'".format(key=call.message.message_id)).fetchall()[0][0]

async def get_payment_values_in_menu_payment(call):
    return cur.execute("SELECT * FROM menu_payment WHERE msg_id == '{key}'".format(key=call.message.message_id)).fetchall()[0]

async def update_value_amount_in_menu_payment(call, value_amount):
    cur.execute("UPDATE menu_payment SET value_amount='{value_amount}' WHERE msg_id='{msg_id}'".format(value_amount=value_amount, msg_id=call.message.message_id))
    db.commit()

async def update_payment_values_in_menu_payment(call, payment_id_or_uuid, sign, order_id, paym_method):
    cur.execute("UPDATE menu_payment SET payment_id_or_uuid='{payment_id_or_uuid}', sign='{sign}', order_id='{order_id}', paym_method='{paym_method}' WHERE msg_id='{msg_id}'".format(msg_id=call.message.message_id, payment_id_or_uuid=payment_id_or_uuid, sign=sign, order_id=order_id, paym_method=paym_method))
    db.commit()
async def del_payment_values_in_menu_payment(call):
    cur.execute(f"DELETE FROM menu_payment WHERE msg_id={call.message.message_id}")
    db.commit()

async def create_tov_menu_info(call):
    cur.execute("INSERT OR IGNORE INTO tov_menu VALUES (?, ?, ?, ?, ?)", (call.message.message_id, call.from_user.id, '', '', ''))
    db.commit()

async def input_tov_menu_info(call, info, work_mode):
    if work_mode == 'category':
        cur.execute("UPDATE tov_menu SET category='{category}' WHERE msg_id='{msg_id}'".format(msg_id=call.message.message_id, category=info))
    elif work_mode == 'subcategory':
        print(f'Полученные данные в функции: msg_id = {call.message.message_id}, info = {info}, work_mode = {work_mode}')
        cur.execute("UPDATE tov_menu SET subcategory='{subcategory}' WHERE msg_id='{msg_id}'".format(msg_id=call.message.message_id, subcategory=info))
        db.commit()
        return cur.execute("SELECT category FROM tov_menu WHERE msg_id == '{key}'".format(key=call.message.message_id)).fetchall()[0][0]
    db.commit()
async def get_count_tov_menu_info(call):
    print(f'get {call.message.message_id}')
    return cur.execute("SELECT * FROM tov_menu WHERE msg_id == '{key}'".format(key=call.message.message_id-1)).fetchall()[0]
async def update_count_tov_menu_info(call, count_tov):
    print(f'update {call.message.message_id} {count_tov}')

    cur.execute("UPDATE tov_menu SET count_tov='{count_tov}' WHERE msg_id='{msg_id}'".format(count_tov=count_tov, msg_id=call.message.message_id-1))
    db.commit()

async def del_tov_menu_info(call):
    cur.execute("DELETE FROM tov_menu WHERE msg_id == '{key}'".format(key=call.message.message_id-1))
    db.commit()