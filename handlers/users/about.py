from aiogram.types import Message
from loader import dp, db
from aiogram.filters import Command
from .translations import messages

@dp.message(Command("about"))
async def about_commands(message:Message):
    lang = db.get_lang(message.from_user.id)
    if lang:
        lang = lang
    else:
        lang = "ru"
    txt = messages[f"about_{lang}"]
    await message.answer(text=txt)