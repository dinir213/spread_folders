async def text_separation(message, text, markup):
    if len(text) > 4095:
        for x in range(0, len(text), 4095):
            await message.answer(text[x:x + 4095], reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)
