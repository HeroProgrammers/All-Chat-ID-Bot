from aiogram.types import Message, FSInputFile, CallbackQuery, InlineKeyboardButton
from loader import dp,db, bot, CHANNELS
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import CommandStart
import asyncio
from keyboard_buttons import user_keyboard
from aiogram import F
from .translations import messages
from filters.check_sub_channel import IsCheckSubChannels

@dp.message(CommandStart())
async def start_command(message:Message):
    
    sticker = FSInputFile("sticker.webp")
    await message.answer_sticker(sticker=sticker)
    await message.answer(text="Made with <b>HeroProgrammers</b>")
    await asyncio.sleep(1)
    print(db.all_users_id())
    if message.from_user.id not in db.all_users_id():


        await message.answer(text="""🇷🇺 Пожалуйста, выберите язык для продолжения!

🇺🇿 Iltimos, davom etish uchun til tanlang!

🇺🇸 Please select a language to continue!""", reply_markup=user_keyboard.lang)

    else:
        user_lang = db.get_lang(message.from_user.id)
        txt = messages[f"start_{user_lang}"]
        await message.answer(text=txt, reply_markup=user_keyboard.menu[user_lang])


@dp.callback_query(F.data.startswith("lang_"))
async def select_language_handler(callback: CallbackQuery):
    full_name = callback.from_user.full_name
    telegram_id = callback.from_user.id
    lang = callback.data.split("_")[1]
    txt = ""
    user_lang = ""
    try:
        db.add_user(telegram_id, full_name, lang)
        user_lang += lang
        txt += messages[f"start_{user_lang}"]
    except:
        db.update_lang(telegram_id, lang)
        user_lang += lang
        txt += messages[f"start_{user_lang}"]
    
    finally:
        await callback.message.delete()
        await callback.message.answer(text=txt, reply_markup=user_keyboard.menu[user_lang])

@dp.callback_query(F.data == "subscribed")
async def subscribed_button_handler(callback: CallbackQuery):
    lang = db.get_lang(callback.from_user.id)
    
    for channel in CHANNELS:
        result = await bot.get_chat_member(channel,callback.from_user.id)
        if result.status in ["member","adminstrator","creator"]:
            await callback.message.edit_text(text=messages[f"checked_channel_yes_{lang}"])

        else:
            await callback.answer(text=messages[f"checked_channel_no_{lang}"], show_alert=True)

@dp.message(IsCheckSubChannels())
async def check_subscribed_channels_handler(message:Message):
    lang = db.get_lang(message.from_user.id)
    text = ""
    inline_channel = InlineKeyboardBuilder()

    for index,channel in enumerate(CHANNELS):
        ChatInviteLink = await bot.create_chat_invite_link(channel)
        inline_channel.add(InlineKeyboardButton(text=f"Hero Programmers",url=ChatInviteLink.invite_link))
    if lang == "uz":
        inline_channel.add(InlineKeyboardButton(text=f"Obuna bo'ldim ✅", callback_data="subscribed"))
    
    if lang == "ru":
        inline_channel.add(InlineKeyboardButton(text=f"Подписался ✅", callback_data="subscribed"))
    
    if lang == "en":
        inline_channel.add(InlineKeyboardButton(text=f"Subscribed ✅", callback_data="subscribed"))
    
    inline_channel.adjust(1,repeat=True)
    button = inline_channel.as_markup()
    text += messages[f"check_channel_{lang}"]
    await message.answer(f"{text}",reply_markup=button)
    

@dp.message(F.text.in_(["♻️ Tilni o'zgartirish", "♻️ Поменять язык", "♻️ Change language"]))
async def change_language_handler(message: Message):
    await message.answer(text="""🇷🇺 Пожалуйста, выберите язык для продолжения!

🇺🇿 Iltimos, davom etish uchun til tanlang!

🇺🇸 Please select a language to continue!""", reply_markup=user_keyboard.lang)

@dp.message(F.text.in_(["🙋🏻‍♂️ Mening IDim", "🙋🏻‍♂️ Мой ID", "🙋🏻‍♂️ My ID"]))
async def own_id_handler(message: Message):
    id = message.from_user.id
    lang = db.get_lang(id)
    text = "🏷 ID: <code>{id}</code>".format(id=id)
    await message.answer(text,reply_markup=user_keyboard.menu[lang])

@dp.message(F.user_shared)
async def get_user_id(message: Message):
    id = message.user_shared.user_id
    lang = db.get_lang(message.from_user.id)
    text = "🏷 ID: <code>{id}</code>".format(id=id)
    await message.answer(text,reply_markup=user_keyboard.menu[lang])

@dp.message(F.chat_shared)
async def get_chat_id(message: Message):
    id = message.chat_shared.chat_id
    lang = db.get_lang(message.from_user.id)
    text = "🏷 ID: <code>{id}</code>".format(id=id)
    await message.answer(text,reply_markup=user_keyboard.menu[lang])
