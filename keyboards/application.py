from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def people_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="1")
    kb.button(text="2")
    kb.button(text="3")
    kb.button(text="4")
    kb.button(text="5")
    kb.button(text="6")
    kb.button(text="Change city")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)


