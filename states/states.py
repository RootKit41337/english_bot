from aiogram.fsm.state import State, StatesGroup


class FSMgame(StatesGroup):
    vvod_word = State() #ожидание состояния ввода слова 
    yes_no_game = State() #ожидание ответа продолжаем игру или нет