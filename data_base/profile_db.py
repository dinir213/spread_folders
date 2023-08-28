from create_bot import db, cur, bot
async def create_profile(message, my_referer):
    user_id = message.from_user.id
    username = message.from_user.username
    user = cur.execute("SELECT * FROM profile WHERE user_id=?", (user_id,)).fetchall()
    if not user:
        cur.execute("INSERT INTO profile VALUES (?, ?, ?, ?, ?)", (user_id, username, 0, my_referer, ''))
        if my_referer != '0':
            my_referals = user_id
            referer_row = cur.execute("SELECT my_referals FROM profile WHERE user_id=?", (my_referer,)).fetchone()
            if referer_row[0] is not None:
                other_referals = referer_row[0]
                my_referals = f"{user_id},{other_referals}"
            await bot.send_message(my_referer, f'По вашей ссылке зарегистрирован пользователь с user_id: {user_id}, username: @{username}\n\nТеперь от каждой его покупки вы будете получать 5%')
            cur.execute("UPDATE profile SET my_referals=? WHERE user_id=?", (my_referals, my_referer))
        db.commit()
    else:
        referer_id = user[0][3]
        print(f'Ваш профиль уже зарегистрирован по ссылке от реферала с user_id: {referer_id}')
async def get_profile(user_id):
    return cur.execute("SELECT * FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
async def edit_profile(call, amount):
    if not isinstance(call, str):
        user_id = call.from_user.id
    else:
        user_id = call
        # Используем параметризованный запрос для извлечения последнего баланса
    last_balance = cur.execute("SELECT balance FROM profile WHERE user_id=?", (user_id,)).fetchone()[0]
    # Используем параметризованный запрос для обновления баланса
    cur.execute("UPDATE profile SET balance=? WHERE user_id=?", (last_balance + float(amount), user_id))
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

async def get_all_users():
    return cur.execute("SELECT user_id FROM profile").fetchall()
async def get_count_all_users():
    return cur.execute("SELECT COUNT(*) FROM profile").fetchone()[0]