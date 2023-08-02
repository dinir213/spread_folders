from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.admin_kb import inline_kb_add_del_tov, inline_kb_add_del_tov_back, print_all_categories
from data_base.admin_db import add_category_db, del_category_db, view_all_categories_db, add_subcategory_db, del_subcategory_db, view_all_subcategories_db, add_position_db, view_all_position_db, del_position_db
import re

class add_del_category(StatesGroup):
    need_action = State()
    start_lvl = State()
    now_lvl = State()
    need_lvl = State()
    target_category = State()
    target_subcategory = State()
    target_position = State()

    price = State()
    description = State()
# class subcategory_full(StatesGroup):
#     price = State()
#     description = State()

async def add_del_tov_main(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f"Выберите, что хотите сделать:\n", reply_markup=inline_kb_add_del_tov)
async def add_del_tov(call: types.CallbackQuery, state: FSMContext):
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
                await call.message.edit_text(f"Выберете название категории:\n", reply_markup=inline_kb_all_categories)
            elif data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название категории:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
        if data['need_lvl'] == 2 or data['need_lvl'] == 3:
            inline_kb_all_categories = await print_all_categories(await view_all_categories_db(), 'category')
            await call.message.edit_text(f"Выберете название категории:\n", reply_markup=inline_kb_all_categories)
    print(f'Метка -0: {await state.get_data()}')


async def choice_btn_in_tovs(call: types.CallbackQuery, state: FSMContext):
    click_btn = call.data.split('_')
    text = click_btn[1]

    async with state.proxy() as data:
        if data['need_lvl'] == 2:
            await state.update_data({"now_lvl": (await state.get_data())['now_lvl'] + 1})
            print(f'Метка Увеличния: {await state.get_data()}')

        print(f'Нажатие кнопки:', click_btn)

        if click_btn[2] == 'category':
            await state.update_data({"target_category": click_btn[1]})
            print(f'Метка 0: {await state.get_data()}')
            target_category = click_btn[1]
        elif click_btn[2] == 'subcategory':
            await state.update_data({"target_subcategory": click_btn[1]})
            print(f'Метка 0.33: {await state.get_data()}')
            target_subcategory = click_btn[1]
            if data['need_lvl'] == 3:
                await state.update_data({"now_lvl": (await state.get_data())['now_lvl'] + 1})
                print(f'Метка Увеличния: {await state.get_data()}')
        elif click_btn[2] == 'position':
            await state.update_data({"target_position": click_btn[1]})
            print(f'Метка 0.67: {await state.get_data()}')
            target_position = click_btn[1]

        need_action = data['need_action']
        now_lvl = (await state.get_data())['now_lvl']
        print(f'Сейчас now_lvl = {now_lvl}')

        if now_lvl == 1:
            print(f'Метка 1: {await state.get_data()}')
            if data['need_lvl'] == 1:
                await del_category_db(data["target_category"])
                await call.message.edit_text(f'Удалена категория с названием {data["target_category"]}', reply_markup=inline_kb_add_del_tov_back)
                print(f'Метка 1.25: {await state.get_data()}')
            elif (data['need_lvl'] == 2 and data['need_action'] == 'add'):
                await state.update_data({"now_lvl": 2})

                print(f'Метка 1.75: {await state.get_data()}')

            elif (data['need_lvl'] == 2 and data['need_action'] == 'del') or data['need_lvl'] == 3:
                # print(f"ЭТо{(await state.get_data())['target_category']}")

                inline_kb_all_subcategories = await print_all_categories(await view_all_subcategories_db((await state.get_data())['target_category']), 'subcategory')
                await call.message.edit_text(f"Выберете название подкатегории:\n", reply_markup=inline_kb_all_subcategories)
                await state.update_data({"now_lvl": 2})
                print(f'Метка 1.5: {await state.get_data()}')



        if now_lvl == 2:
            if data['need_lvl'] == 2 and data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название подкатегории:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
                print(f'Метка 2: {await state.get_data()}')

            elif data['need_lvl'] == 2 and data['need_action'] == 'del':
                print(f'Метка 3: {await state.get_data()}')
                await del_subcategory_db((await state.get_data())['target_category'], (await state.get_data())['target_subcategory'])
                inline_kb_all_subcategories = await print_all_categories(await view_all_subcategories_db(data['target_category']), 'subcategory')
                await call.message.edit_reply_markup(inline_kb_all_subcategories)

            elif data['need_lvl'] == 3 and data['need_action'] == 'add':
                print(f'Метка 4: {await state.get_data()}')
                await state.update_data({"now_lvl": 3})

            elif data['need_lvl'] == 3 and data['need_action'] == 'del':
                print(f'Метка 5: {await state.get_data()}')
                # inline_kb_all_subcategories = await print_all_categories(await view_all_subcategories_db((await state.get_data())['target_category']), 'subcategory')
                # await call.message.edit_text(f"Выберете название позиции:\n", reply_markup=inline_kb_all_subcategories)
                await state.update_data({"now_lvl": 3})
                await call.message.edit_text(f"Введите номер позиции, который желаете удалить:\n")

        elif now_lvl == 3:
            if data['need_action'] == 'add':
                print(f'Метка 6: {await state.get_data()}')
                await call.message.edit_text(f"Введите название ПОЗИЦИИ:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
            elif data['need_action'] == 'del':
                # target_subcategory = (await state.get_data())['target_subcategory']
                # await del_position_db(target_subcategory, click_btn[1])
                # inline_kb_all_position = await print_all_categories(await view_all_position_db(target_subcategory), 'position')
                await call.message.edit_text(f"Введите номер позиции, который желаете удалить:\n", reply_markup=inline_kb_add_del_tov_back)
                print(f'Метка 7: {await state.get_data()}')
                await add_del_category.target_subcategory.set()


async def add_tov(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print('Мы зашли в стейт2')

        print(f'Метка 14: {await state.get_data()}\n{message.text}')

        text = message.text
        if data['need_lvl'] == 1:
            await add_category_db(text)
        elif data['need_lvl'] == 2:
            await state.update_data({"target_subcategory": message.text})
            await message.answer('Теперь введи цену товара', reply_markup=inline_kb_add_del_tov_back)
            await add_del_category.price.set()
        elif data['need_lvl'] == 3:
            positions = re.split("\s+|\n", message.text)
            if len(positions) % 3 == 0:
                cycles = len(positions) / 3

                print(f'len(positions) = {len(positions)}, range(cycles) = {range(int(cycles))}')
                for i in range(int(cycles)):
                    print(positions[i+0], positions[i+1], positions[i+2])
                    await add_position_db(data['target_subcategory'], positions[i+0], positions[i+1], positions[i+2], data['target_category'])
                    i = i + 3
                await state.finish()
            else:
                await message.answer('Введи еще раз', reply_markup=inline_kb_add_del_tov_back)


async def add_tov_fill_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
        await message.answer('Теперь введи описание товара', reply_markup=inline_kb_add_del_tov_back)
        await add_del_category.description.set()
async def add_tov_fill_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await state.update_data({"description": message.text})

        print(f'Метка 15: {await state.get_data()}')
        await add_subcategory_db(data['target_category'], data['target_subcategory'], float(data['price']), data['description'])
        await state.finish()
async def del_tov(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        target_position = message.text
        need_lvl = (await state.get_data())['need_lvl']
        # if data['need_lvl'] == 2:
        #     await del_subcategory_db(data['target_category'], data['target_subcategory'])
        #     inline_kb_all_subcategories = await print_all_categories(await view_all_subcategories_db(data['target_category']), 'subcategory')
        #     await call.message.edit_reply_markup(inline_kb_all_subcategories)
        if need_lvl == 3:
            # data['target_position'] = call.data.split('_')[1]
            print(f'Метка 16: {await state.get_data()}')
            print('Мы зашли в стейт1')
            await del_position_db(data['target_subcategory'], target_position)
            # inline_kb_all_position = await print_all_position(await view_all_position_db(data['target_subcategory']))
            # await call.message.edit_reply_markup(inline_kb_all_position)
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(add_del_tov_main, text_startswith="add_del_tov", state='*')
    dp.register_callback_query_handler(add_del_tov, text_startswith="btn_")
    dp.register_callback_query_handler(choice_btn_in_tovs, text_startswith="del_", state="*")
    dp.register_message_handler(add_tov, state=add_del_category.target_category)
    dp.register_message_handler(add_tov_fill_price, state=add_del_category.price)
    dp.register_message_handler(add_tov_fill_desc, state=add_del_category.description)

    dp.register_message_handler(del_tov, state=add_del_category.target_subcategory)
