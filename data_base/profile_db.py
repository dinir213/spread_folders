from create_bot import db, cur
async def create_profile(message):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=message.from_user.id)).fetchone()
    if not user:
        cur.execute(f"INSERT INTO profile VALUES (?, ?, ?)", (message.from_user.id, message.from_user.username, 0))
        db.commit()

async def get_profile(user_id):
    # print(cur.execute(f"SELECT * FROM profile").fetchall())
    return cur.execute("SELECT * FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
async def edit_profile(call, amount):
    last_balance = float(cur.execute("SELECT balance FROM profile WHERE user_id == '{key}'".format(key=call.from_user.id)).fetchall()[0][0])
    new_balance = last_balance + float(amount)
    cur.execute("UPDATE profile SET balance='{balance}' WHERE user_id='{user_id}'".format(user_id=call.from_user.id, balance=new_balance))
    db.commit()
