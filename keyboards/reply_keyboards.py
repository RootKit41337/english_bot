from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton


start_mr = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "Жмякни если хочешь играть!😍"),
            KeyboardButton(text= 'Жмякни если не хочешь играть🥲')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
) 

otvet_mr = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "Я хочу играть до победного😈"),
            KeyboardButton(text= 'Я не хочу играть🥲')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    selective=True
)