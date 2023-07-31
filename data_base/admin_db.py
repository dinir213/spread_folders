from create_bot import db, cur
async def view_all_payment_methods():
    return cur.execute("SELECT * FROM payment_methods")
async def turn_payment_method_db(work_mode, payment_name):
    cur.execute(f"UPDATE payment_methods SET work_mode={work_mode} WHERE payment_name='{payment_name}'")
    db.commit()