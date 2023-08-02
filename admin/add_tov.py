from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.admin_kb import inline_kb_add_del_tov, inline_kb_add_del_tov_back, print_all_categories, print_all_subcategories, print_all_position
from data_base.admin_db import add_category_db, del_category_db, view_all_categories_db, add_subcategory_db, del_subcategory_db, view_all_subcategories_db, add_position_db, view_all_position_db, del_position_db

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
                inline_kb_all_categories = await print_all_categories(await view_all_categories_db())
                await call.message.edit_text(f"Выберете название категории:\n", reply_markup=inline_kb_all_categories)
            elif data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название категории:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
        if data['need_lvl'] == 2 or data['need_lvl'] == 3:
            inline_kb_all_categories = await print_all_categories(await view_all_categories_db())
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

                inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db((await state.get_data())['target_category']))
                await call.message.edit_text(f"Выберете название подкатегории:\n", reply_markup=inline_kb_all_subcategories)
                await state.update_data({"now_lvl": 2})
                print(f'Метка 1.5: {await state.get_data()}')



        if now_lvl == 2:
            if data['need_lvl'] == 2 and data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название подкатегории:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
                # inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db(data['target_category']))
                # await call.message.edit_reply_markup(reply_markup=inline_kb_all_subcategories)
                print(f'Метка 2: {await state.get_data()}')

            elif data['need_lvl'] == 2 and data['need_action'] == 'del':
                print(f'Метка 3: {await state.get_data()}')
                await del_subcategory_db((await state.get_data())['target_category'], (await state.get_data())['target_subcategory'])
                inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db(data['target_category']))
                await call.message.edit_reply_markup(inline_kb_all_subcategories)

            elif data['need_lvl'] == 3 and data['need_action'] == 'add':
                print(f'Метка 4: {await state.get_data()}')
                await state.update_data({"now_lvl": 3})

            elif data['need_lvl'] == 3 and data['need_action'] == 'del':
                print(f'Метка 5: {await state.get_data()}')
                inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db((await state.get_data())['target_category']))
                await call.message.edit_text(f"Выберете название позиции:\n", reply_markup=inline_kb_all_subcategories)
                await state.update_data({"now_lvl": 3})
        elif now_lvl == 3:
            if data['need_action'] == 'add':
                await call.message.edit_text(f"Введите название ПОЗИЦИИ:\n", reply_markup=inline_kb_add_del_tov_back)
                await add_del_category.target_category.set()
            elif data['need_action'] == 'del':
                target_subcategory = (await state.get_data())['target_subcategory']
                await del_position_db(target_subcategory, click_btn[1])
                inline_kb_all_position = await print_all_position(await view_all_position_db(target_subcategory))
                await call.message.edit_reply_markup(reply_markup=inline_kb_all_position)




        # Это первый нудачный код
        # print(f'Метка 1: {await state.get_data()}')
        # await state.get_state()
        # if data['now_lvl'] == 1:
        #     print(f'Метка 2: {await state.get_data()}')
        #
        #     data['target_category'] = text
        #     data['now_lvl'] = 2
        #     if data['need_lvl'] == 1:
        #         if need_action == 'del':
        #             print(f'Метка 3: {await state.get_data()}')
        #
        #             await del_category_db(text)
        #             await call.message.edit_text(f'Удалена категория с названием {text}', reply_markup=inline_kb_add_del_tov_back)
        #
        # elif data['now_lvl'] == 2:
        #     print(f'Метка 4: {await state.get_data()}')
        #
        #     # data['target_subcategory'] = text
        #     print('Сабкатегория: ', text)
        #     print(f'Метка 5: {await state.get_data()}')
        #
        #     if data['need_lvl'] == 2:
        #         if need_action == 'del':
        #             print(f'Метка 6: {await state.get_data()}')
        #
        #             inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db(data['target_category']))
        #             await call.message.edit_text(f"Выберете название подкатегории:\n", reply_markup=inline_kb_all_subcategories)
        #             await add_del_category.target_subcategory.set()
        #
        #         elif need_action == 'add':
        #             print(f'Метка 7: {await state.get_data()}')
        #
        #             await call.message.edit_text(f"Введите название подкатегории:\n", reply_markup=inline_kb_add_del_tov_back)
        #             await add_del_category.target_category.set()
        #             # await add_tov(message=call.message, state=state)
        #
        #     elif data['need_lvl'] == 3:
        #         print(f'Метка 8: {await state.get_data()}')
        #
        #         inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db(data['target_category']))
        #         await call.message.edit_text(f"Выберете название подкатегории:\n", reply_markup=inline_kb_all_subcategories)
        #         data['now_lvl'] = 3
        #         print(f'Метка 9: {await state.get_data()}')
        #
        #
        # elif data['now_lvl'] == 3:
        #     print(f'Метка 10: {await state.get_data()}')
        #
        #     # data['target_position'] = text
        #     print(f'Метка 11: {await state.get_data()}')
        #
        #     if data['need_lvl'] == 3:
        #         if need_action == 'del':
        #             print(f'Метка 12: {await state.get_data()}')
        #
        #             inline_kb_all_position = await print_all_position(await view_all_position_db(data['target_subcategory']))
        #             # await call.message.edit_text(f"Выберете название позиции:\n", reply_markup=inline_kb_all_position)
        #             await call.message.edit_text(f"Выберете название позиции:\n", reply_markup=inline_kb_all_position)
        #
        #             await add_del_category.target_subcategory.set()
        #
        #         elif need_action == 'add':
        #             print(f'Метка 13: {await state.get_data()}')
        #
        #             await call.message.edit_text(f"Введите название позиции:\n", reply_markup=inline_kb_add_del_tov_back)
        #             # await add_tov(message=call.message, state=state)
        #             await add_del_category.target_category.set()

async def add_tov(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        print(f'Метка 14: {await state.get_data()}\n{message.text}')

        text = message.text
        if data['need_lvl'] == 1:
            await add_category_db(text)
        elif data['need_lvl'] == 2:
            await state.update_data({"target_subcategory": message.text})
            await message.answer('Теперь введи цену товара', reply_markup=inline_kb_add_del_tov_back)
            await add_del_category.price.set()
        elif data['need_lvl'] == 3:
            await add_position_db(data['target_subcategory'], message.text.split(' '))

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
async def del_tov(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['need_lvl'] == 2:
            await del_subcategory_db(data['target_category'], data['target_subcategory'])
            inline_kb_all_subcategories = await print_all_subcategories(await view_all_subcategories_db(data['target_category']))
            await call.message.edit_reply_markup(inline_kb_all_subcategories)
        elif data['need_lvl'] == 3:
            # data['target_position'] = call.data.split('_')[1]
            print(f'Метка 16: {await state.get_data()}')

            await del_position_db(data['target_subcategory'], data['target_position'])
            # inline_kb_all_position = await print_all_position(await view_all_position_db(data['target_subcategory']))
            # await call.message.edit_reply_markup(inline_kb_all_position)
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(add_del_tov_main, text_startswith="add_del_tov", state='*')
    dp.register_callback_query_handler(add_del_tov, text_startswith="btn_")
    dp.register_callback_query_handler(choice_btn_in_tovs, text_startswith="del_", state="*")
    dp.register_message_handler(add_tov, state=add_del_category.target_category)
    dp.register_message_handler(add_tov_fill_price, state=add_del_category.price)
    dp.register_message_handler(add_tov_fill_desc, state=add_del_category.description)

    dp.register_callback_query_handler(del_tov, state=add_del_category.target_subcategory)
