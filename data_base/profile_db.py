from create_bot import db, cur
async def create_profile(message):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=message.from_user.id)).fetchone()
    if not user:
        cur.execute(f"INSERT INTO profile VALUES (?, ?, ?)", (message.from_user.id, message.from_user.username, 0))
        db.commit()

async def get_profile(user_id):
    # print(cur.execute(f"SELECT * FROM profile").fetchall())
    return cur.execute("SELECT * FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
