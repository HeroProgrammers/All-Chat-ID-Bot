from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
													 ReplyKeyboardMarkup, KeyboardButton, )
from aiogram.types import KeyboardButtonRequestChat, KeyboardButtonRequestUser

lang = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="🇷🇺", callback_data="lang_ru"),
			InlineKeyboardButton(text="🇺🇿", callback_data="lang_uz"),
			InlineKeyboardButton(text="🇺🇸",callback_data="lang_en")
		]
	]
)

menu = {
	"uz": ReplyKeyboardMarkup(
		keyboard=[
		[
			KeyboardButton(text="🙋🏻‍♂️ Mening IDim")
		],
		[
			KeyboardButton(text="👤 Foydalanuvchi",request_user=KeyboardButtonRequestUser(request_id=1,user_is_bot=False)),
			KeyboardButton(text="🤖 Bot",request_user=KeyboardButtonRequestUser(request_id=2,user_is_bot=True))
		],
		[
			KeyboardButton(text="👥 Guruh",request_chat=KeyboardButtonRequestChat(request_id=3,chat_is_channel=False)),
			KeyboardButton(text="📢 Kanal",request_chat=KeyboardButtonRequestChat(request_id=4,chat_is_channel=True))
		],
		[
			KeyboardButton(text="♻️ Tilni o'zgartirish")
		]


    ],
		resize_keyboard=True
	),

	"ru": ReplyKeyboardMarkup(
		keyboard=[
		[
			KeyboardButton(text="🙋🏻‍♂️ Мой ID")
		],
		[
			KeyboardButton(text="👤 Пользователь",request_user=KeyboardButtonRequestUser(request_id=1,user_is_bot=False)),
			KeyboardButton(text="🤖 Бот",request_user=KeyboardButtonRequestUser(request_id=2,user_is_bot=True))
		],
		[
			KeyboardButton(text="👥 Группа",request_chat=KeyboardButtonRequestChat(request_id=3,chat_is_channel=False)),
			KeyboardButton(text="📢 Канал",request_chat=KeyboardButtonRequestChat(request_id=4,chat_is_channel=True))
		],
		[
			KeyboardButton(text="♻️ Поменять язык")
		]


    ],
		resize_keyboard=True
	),
	
	"en": ReplyKeyboardMarkup(
		keyboard=[
		[
			KeyboardButton(text="🙋🏻‍♂️ My ID")
		],
		[
			KeyboardButton(text="👤 User",request_user=KeyboardButtonRequestUser(request_id=1,user_is_bot=False)),
			KeyboardButton(text="🤖 Bot",request_user=KeyboardButtonRequestUser(request_id=2,user_is_bot=True))
		],
		[
			KeyboardButton(text="👥 Group",request_chat=KeyboardButtonRequestChat(request_id=3,chat_is_channel=False)),
			KeyboardButton(text="📢 Channel",request_chat=KeyboardButtonRequestChat(request_id=4,chat_is_channel=True))
		],
		[
			KeyboardButton(text="♻️ Change language")
		]

    ],
		resize_keyboard=True
	),
}