from aiogram.fsm.state import State, StatesGroup


# Initialize states


class Forecast(StatesGroup):
    """
    States for forecast flow
    """
    city_choice = State()
    date_choice = State()
    result = State()


class Application(StatesGroup):
    """
    States for application flow
    """
    city_choice = State()
    people_num_choice = State()
    budget_choice = State()
    date_choice = State()
    duration_choice = State()
    name = State()
    phone = State()
    final = State()