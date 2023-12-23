from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


main_menu_button_text = "Back to main menu"

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


def budget_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Change number of people")
    kb.button(text=main_menu_button_text)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def trip_date_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Change budget")
    kb.button(text=main_menu_button_text)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def trip_duration_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="2")
    kb.button(text="5")
    kb.button(text="7")
    kb.button(text="10")
    kb.button(text="14")
    kb.button(text="20")
    kb.button(text="Change start date")
    kb.button(text=main_menu_button_text)
    kb.adjust(3,3,1,1)
    return kb.as_markup(resize_keyboard=True)

def username_kb() -> ReplyKeyboardMarkup:
    kb.button(text="Change trip duration")
    kb.button(text=main_menu_button_text)
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)