import time

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.admin_kb import inline_kb_add_del_tov, inline_kb_add_del_tov_back, print_all_categories
from data_base.admin_db import add_category_db, del_category_db, view_all_categories_db, add_subcategory_db, del_subcategory_db, view_all_subcategories_db, add_position_db, view_all_position_db, del_position_db, update_count_tovs_db
from Special_funcs.funcs import text_separation
import re
from create_bot import bot
import secrets
import string

class add_del_category(StatesGroup):
    need_action = State()
    start_lvl = State()
    now_lvl = State()
    need_lvl = State()
    target_category = State()
    target_subcategory = State()
    target_position = State()

    img_code = State()
    price = State()
    description = State()

async def add_del_tov_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"Выберите, что хотите сделать:\n", reply_markup=inline_kb_add_del_tov)
async def add_del_tov(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    work_config = call.data.split('_') # Приходит ['btn', 'add', 'subcategory'] - первый индекс значит добавление, а второй индекс - подкатегория
    async with state.proxy() as data:
        data['need_action'] = work_config[1]
        data['now_lvl'] = 1
        if work_config[2] == 'category':
            data['need_lvl'] = 1
        elif work_config[2] == 'subcategory':
            data['need_lvl'] = 2
        elif work_config[2] == 'position':
            data['need_lvl'] = 3

        if data['need_lvl'] == 1:
            if data['need_action'] == 'del':
                inline_kb_all_categories = await print_all_categories(await view_all_categories_db(), 'category')
                if inline_kb_all_categories[1] == 1:
                    await call.message.edit_text(f"Выберете название категории:\n", reply_markup=inline_kb_all_categories[0])
                else:
                    await call.message.edit_text(f"Вы пока не создали ни одну категорию товаров. Перед созданием подкатегории создайте категорию товаров\n", reply_markup=inline_kb_add_del_tov_back)

            elif data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название категории:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
        if data['need_lvl'] == 2 or data['need_lvl'] == 3:
            inline_kb_all_categories = await print_all_categories(await view_all_categories_db(), 'category')
            if inline_kb_all_categories[1] == 1:
                print(f"Ошибочная клавиатура: {inline_kb_all_categories}")
                await call.message.edit_text(f"Выберете название категории:\n", reply_markup=inline_kb_all_categories[0])
            else:
                await call.message.edit_text(f"Вы пока не создали ни одну категорию товаров. Перед созданием/удалением подкатегории/позиции создайте категорию товаров\n", reply_markup=inline_kb_add_del_tov_back)

async def choice_btn_in_tovs(call: types.CallbackQuery, state: FSMContext):
    click_btn = call.data.split('~')
    text = click_btn[1]

    async with state.proxy() as data:
        if data['need_lvl'] == 2:
            await state.update_data({"now_lvl": (await state.get_data())['now_lvl'] + 1})

        if click_btn[2] == 'category':
            await state.update_data({"target_category": click_btn[1]})
            target_category = click_btn[1]
        elif click_btn[2] == 'subcategory':
            await state.update_data({"target_subcategory": click_btn[1]})
            target_subcategory = click_btn[1]
            if data['need_lvl'] == 3:
                await state.update_data({"now_lvl": (await state.get_data())['now_lvl'] + 1})
        elif click_btn[2] == 'position':
            await state.update_data({"target_position": click_btn[1]})
            target_position = click_btn[1]

        need_action = data['need_action']
        now_lvl = (await state.get_data())['now_lvl']

        if now_lvl == 1:
            if data['need_lvl'] == 1:
                await del_category_db(target_category)
                await call.message.edit_text(f'Категория {target_category} успешно удалена Администратором {call.from_user.username} ✅', reply_markup=inline_kb_add_del_tov_back)
            elif (data['need_lvl'] == 2 and data['need_action'] == 'add'):
                await state.update_data({"now_lvl": 2})
            elif (data['need_lvl'] == 2 and data['need_action'] == 'del') or data['need_lvl'] == 3:
                target_category = (await state.get_data())['target_category']

                inline_kb_all_subcategories = await print_all_categories(await view_all_subcategories_db(target_category), 'subcategory')
                if inline_kb_all_subcategories[1] == 1:
                    await call.message.edit_text(f"Выберете название подкатегории:\n", reply_markup=inline_kb_all_subcategories[0])
                    await state.update_data({"now_lvl": 2})
                else:
                    await call.message.edit_text(f"Подкатегорий товаров нету, вы можете создать из, вернувшись назад\n", reply_markup=inline_kb_add_del_tov_back)

        if now_lvl == 2:
            if data['need_lvl'] == 2 and data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название подкатегории:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()

            elif data['need_lvl'] == 2 and data['need_action'] == 'del':
                await del_subcategory_db((await state.get_data())['target_category'], target_subcategory)
                await update_count_tovs_db(+1, 'category', data['target_category'], data['target_subcategory'])

                inline_kb_all_subcategories = await print_all_categories(await view_all_subcategories_db(data['target_category']), 'subcategory')
                if inline_kb_all_subcategories[1] == 1:
                    await call.message.edit_reply_markup(inline_kb_all_subcategories[0])
                else:
                    await call.message.edit_text(f"В данной категории товаров удалены все подкатегории\n", reply_markup=inline_kb_add_del_tov_back)

            elif data['need_lvl'] == 3 and data['need_action'] == 'add':
                await state.update_data({"now_lvl": 3})
            elif data['need_lvl'] == 3 and data['need_action'] == 'del':
                await state.update_data({"now_lvl": 3})
                await call.message.edit_text(f"Введите номер позиции, который желаете удалить:\n")

        elif now_lvl == 3:
            if data['need_action'] == 'add':
                await call.message.edit_text(f"Вводите позиции по три значения в одну позицию(Логин Ключ Резерв)\nЧтобы ввести много строк товара, пишите следующим образом:\n\nЛОГИН1 ПАРОЛЬ1 РЕЗЕРВ1 ЛОГИН2 ПАРОЛЬ2 РЕЗЕРВ2 ЛОГИН3 ПАРОЛЬ3 РЕЗЕРВ3\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
            elif data['need_action'] == 'del':
                target_subcategory = (await state.get_data())['target_subcategory']
                all_positions = await view_all_position_db(target_subcategory)
                if all_positions != []:
                    all_positions_str = ''
                    for position in all_positions:
                        all_positions_str = f'{all_positions_str}/Delete_{position[0]} {position[1]} {position[2]} {position[3]}\n'
                    all_positions_str = 'Выберите ID строки с данными, которую желаете удалить\n\n/Delete_all - Нажмите, если желаете удалить все позиции в подкатегории\n' + all_positions_str
                else:
                    all_positions_str = f'Позиций в подкатегории {target_subcategory} нет'
                if len(all_positions_str) < 4095:
                    await call.message.edit_text(all_positions_str, reply_markup=inline_kb_add_del_tov_back)
                else:
                    for x in range(0, len(all_positions_str), 4095):
                        await call.message.answer(all_positions_str[x:x + 4095], reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_subcategory.set()
        await call.answer()

async def add_tov(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        text = message.text
        if data['need_lvl'] == 1:
            if len(text) <= 18:
                await add_category_db(text)
                await message.answer(f'Категория {text} создана Администратором {message.from_user.username} ✅',reply_markup=inline_kb_add_del_tov_back)
                await state.finish()
            else:
                await message.answer(f"Количество символов в названии не должно превышать 18 символов\nВведите повторно:", reply_markup=inline_kb_add_del_tov_back)
        elif data['need_lvl'] == 2:
            target_subcategory = text
            if len(target_subcategory) <= 18:
                await state.update_data({"target_subcategory": target_subcategory})
                await message.answer('Теперь отправь фото товара', reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.img_code.set()
            else:
                await message.answer(f"Количество символов в названии не должно превышать 18 символов\nВведите повторно:", reply_markup=inline_kb_add_del_tov_back)

        elif data['need_lvl'] == 3:
            positions = re.split("\s+|\n", message.text)
            if len(positions) % 3 == 0:
                cycles = len(positions) / 3
                result = 'Вы добавили следующие товары:\n'
                i = 0
                j = 0
                timestart = time.perf_counter()
                data_for_bd = []
                while j < cycles:
                    # await add_position_db(data['target_subcategory'], positions[i], positions[i + 1], positions[i + 2] ,data['target_category'])
                    data_append = (positions[i], positions[i + 1], positions[i + 2])
                    print(data_append)
                    data_for_bd.append(data_append)
                    print(data_for_bd)
                    result = f'{result}{j + 1}. Логин: {positions[i]}, Пароль: {positions[i + 1]}, Резерв: {positions[i + 2]}\n'
                    i = i + 3
                    j = j + 1
                await add_position_db(data['target_subcategory'], data_for_bd, data['target_category'])

                await update_count_tovs_db(+1, 'subcategory', data['target_category'], data['target_subcategory'])
                await text_separation(message, result, inline_kb_add_del_tov_back)
                idle = time.perf_counter() - timestart
                print(idle)
                await state.finish()
            else:
                await message.answer('Введите значения еще раз, количество элементов должно быть кратно трём', reply_markup=inline_kb_add_del_tov_back)

async def add_tov_fill_photo(message: types.Message, state: FSMContext):
    N = 12
    img_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                  for i in range(N))
    await state.update_data({"img_code": img_code})
    await message.photo[-1].download(destination_file=f'imgs/{img_code}.jpg')
    await message.answer('Теперь введи цену товара(если значение дробное, используйте ".", но не ",")', reply_markup=inline_kb_add_del_tov_back)
    await add_del_category.price.set()


async def add_tov_fill_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['price'] = float(message.text)
            await message.answer('Теперь введи описание товара', reply_markup=inline_kb_add_del_tov_back)
            await add_del_category.description.set()
        except:
            await message.answer('Вы ввели цену неверно', reply_markup=inline_kb_add_del_tov_back)

async def add_tov_fill_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        description = message.text
        await add_subcategory_db(data['target_category'], data['target_subcategory'], float(data['price']), description, data['img_code'])
        await update_count_tovs_db(+1, 'category', data['target_category'], data['target_subcategory'])
        photo = InputFile(f"imgs/{data['img_code']}.jpg")
        await bot.send_photo(message.chat.id, photo=photo, caption=f"<b>💎 Категория:</b> <i>{data['target_category']}</i>\n<b>💎 Подкатегория:</b> <i>{data['target_subcategory']}</i>\n<b>💰 Цена:</b> <i>{data['price']} руб</i>\n<b>📀 На складе:</b> <i>0 шт.</i>\n<b>💚 Описание:</b> <i>{description}</i>", parse_mode='html')
        await state.finish()
async def del_tov(message: types.Message, state: FSMContext):
    need_lvl = (await state.get_data())['need_lvl']
    target_positions = message.text.split('_')
    if need_lvl == 3 and target_positions[0] == '/Delete':
        timestart = time.perf_counter()
        target_subcategory = (await state.get_data())['target_subcategory']
        target_category = (await state.get_data())['target_category']
        idle = time.perf_counter() - timestart
        print(idle)
        try:
            target_positions[1] = int(target_positions[1])
            await del_position_db(target_subcategory, target_positions[1])
        except:
            if target_positions[1] == 'all':
                await del_position_db(target_subcategory, 'all')
        await update_count_tovs_db(-1, 'subcategory', target_category, target_subcategory)
        await message.delete()
        all_positions_str = f'Позиции в категории {target_category} и в подкатегории {target_subcategory} успешно удалены Администратором {message.from_user.username} ✅! '
        await message.answer(all_positions_str, reply_markup=inline_kb_add_del_tov_back)
        await state.finish()
    else:
        await message.answer('Произошла ошибка, попробуйте еще раз', reply_markup=inline_kb_add_del_tov_back)

def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(add_del_tov_main, text_startswith="add_del_tov", state='*')
    dp.register_callback_query_handler(add_del_tov, text_startswith="btn_")
    dp.register_callback_query_handler(choice_btn_in_tovs, text_startswith="change~", state="*")
    dp.register_message_handler(add_tov, state=add_del_category.target_category)
    dp.register_message_handler(add_tov_fill_photo, state=add_del_category.img_code, content_types=['photo'])
    dp.register_message_handler(add_tov_fill_price, state=add_del_category.price)
    dp.register_message_handler(add_tov_fill_desc, state=add_del_category.description)
    dp.register_message_handler(del_tov, state=add_del_category.target_subcategory)
