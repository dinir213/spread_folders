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