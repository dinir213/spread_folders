from create_bot import db, cur


def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, username TEXT, balance REAL)")
    db.commit()
