from create_bot import db, cur, bot
async def create_profile(message, my_referer):
    user = cur.execute("SELECT * FROM profile WHERE user_id == '{key}'".format(key=message.from_user.id)).fetchall()
    if not user:
        cur.execute(f"INSERT INTO profile VALUES (?, ?, ?, ?, ?)", (message.from_user.id, message.from_user.username, 0, my_referer, ''))
        if my_referer != '0':

            if (cur.execute("SELECT my_referals FROM profile WHERE user_id=='{user_id}'".format(user_id=my_referer)).fetchone())[0] is not None:
                other_referals = cur.execute("SELECT my_referals FROM profile WHERE user_id=='{user_id}'".format(user_id=my_referer)).fetchone()[0]
                print(other_referals)
                my_referals = str(message.from_user.id) + ',' + other_referals
            else:
                my_referals = message.from_user.id
            await bot.send_message(my_referer, f'По вашей ссылке зарегистрирован пользователь с user_id: {message.from_user.id}, username: @{message.from_user.username}\n\nТеперь от каждой его покупки вы будете получать 5%')
            cur.execute("UPDATE profile SET my_referals='{my_referals}' WHERE user_id='{my_referer}'".format(my_referer=my_referer, my_referals=my_referals))
        db.commit()
    else:
        print(f'Ваш профиль уже зарегистрирован по ссылке от реферала с user_id: {user[0][3]}')

async def get_profile(user_id):
    # print(cur.execute(f"SELECT * FROM profile").fetchall())
    return cur.execute("SELECT * FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
async def edit_profile(call, amount):
    last_balance = float(cur.execute("SELECT balance FROM profile WHERE user_id == '{key}'".format(key=call.from_user.id)).fetchall()[0][0])
    new_balance = last_balance + float(amount)
    cur.execute("UPDATE profile SET balance='{balance}' WHERE user_id='{user_id}'".format(user_id=call.from_user.id, balance=new_balance))
    db.commit()
# Работа с рефералами:

async def check_args(referer, user_id: int):
    if referer == '':
        return '0'
    elif not referer.isnumeric():
        return '0'
    elif referer.isnumeric():
        profile_referer = await get_profile(user_id=int(referer))
        if int(referer) == user_id:
            return '0'
        elif profile_referer is None:
            print(f'Пользователь с id={referer}, который тебя пригласил, не существует')
            return '0'
        else:
            i = 1
            for referal in (profile_referer[4]).split(','):
                print(f'{i}. {referal}\nreferal={referal}, user_id={user_id}')
                i = i + 1
                if str(referal) == str(user_id):
                    print(f'У пригласившего вас пользователя найден user_id, равный вашему: {referer}=={user_id}')
                    return '0'
            return str(referer)
    else:
        return '0'

