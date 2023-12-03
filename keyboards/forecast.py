from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def date_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Tomorrow")
    kb.button(text="Change city")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


