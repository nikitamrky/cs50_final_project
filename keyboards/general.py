from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Yes")
    kb.button(text="No")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def fcast_or_app_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Forecast")
    kb.button(text="Application")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)