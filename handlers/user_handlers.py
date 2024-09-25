from copy import deepcopy

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext


from lexicon.lexicon import LEXICON_RU, LEXICON_LENG, LEXICON_MAIN
from filters.is_admin import IsAdmin
from states.states import *

from config_data.config import Config, load_config
from keyboards.reply_keyboards import start_mr, otvet_mr
from services.services import *
from database.users import *


router = Router()
config: Config = load_config()



@router.message(CommandStart(), StateFilter(default_state)) # IsAdmin(config.tg_bot.admin_ids),
async def start_message(message: Message):
    await handle_new_user(message)
    await message.answer(text = LEXICON_RU['/start'], reply_markup=start_mr)
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(users_template)


@router.message(Command('help'), StateFilter(default_state))
async def help_massage(message: Message):
    await message.answer(text = LEXICON_RU['/help'])


bot_otv = random_word()
@router.message(F.text.in_(['Жмякни если хочешь играть!😍']), StateFilter(default_state))
async def knopka_emae(message: Message, state: FSMContext):
    global bot_otv
    await message.answer(f'Вот твое слово, переведи его🗿\n\n                   <b>{bot_otv}</b>')
    await state.set_state(FSMgame.vvod_word)
    # if message.from_user.id not in users_db:
    #     users_db[message.from_user.id] = deepcopy(users_template)

#TODO: это чтобы люди не пытались использовать
@router.message(F.text.in_(['/start', '/help']), StateFilter(FSMgame.yes_no_game))
async def otv_game_com(message: Message):
    await message.answer(text= 'К сожалению эта команда не водоступна во время игры...\nЧтобы воспользоваться командой нажми на <b><i><u>Я не хочу играть🥲</u></i></b>')

@router.message(F.text.in_(['/start', '/help']), StateFilter(FSMgame.vvod_word))
async def otv_game_com(message: Message):
    global bot_otv
    await message.answer(text= 'К сожалению эта команда не водоступна во время игры...\nЧтобы воспользоваться командой сначала переведи предложенное слово, а потом нажми на кнопку\n<b><i><u>Я не хочу играть🥲</u></i></b> открыв меню кнопок🤯')
    await message.answer(f'Напоминаю слово:\n\n         <b>{bot_otv}</b>')

@router.message(F.text == 'Жмякни если не хочешь играть🥲', StateFilter(default_state))
async def no_otv(message: Message):
    await message.answer(text = 'Если захожешь играть то жмякни на кнопку\n<b><i>Жмякни если хочешь играть!😍</i></b>', reply_markup=start_mr)

def obnov(bot_otv):
    bot_otv = random_word()
    return bot_otv

@router.message(F.text, StateFilter(FSMgame.vvod_word))
async def hhhh(message: Message, state:FSMContext):
    global bot_otv
    user_otv = message.text
    user_otv = user_otv.lower()
    winner = check_answer(user_otv, bot_otv)
    if winner == 'Молодец\n\nТы ответил правильно😍':
        user_score = users_db[message.from_user.id]['score']
        user_score += 1
        users_db[message.from_user.id]['score'] = user_score
        user_life = users_db[message.from_user.id]['life']
        await message.answer(f'{winner}\n\nТвой счет {user_score}\nТвои жизни {user_life}❤️', reply_markup=otvet_mr) #\n\nТвой счет {user_score}
        bot_otv = obnov(bot_otv)
        await state.set_state(FSMgame.yes_no_game)
    else:      
        user_life = users_db[message.from_user.id]['life']
        user_life -= 1
        users_db[message.from_user.id]['life'] = user_life
        if users_db[message.from_user.id]['life'] != 0:
            user_score = users_db[message.from_user.id]['score']
            await message.answer(f'{winner}\n\nТвой счет {user_score}\nТвои жизни {user_life}❤️', reply_markup=otvet_mr) #\n\nТвой счет {user_score}
            bot_otv = obnov(bot_otv)
            await state.set_state(FSMgame.yes_no_game)
        else:
            user_score = users_db[message.from_user.id]['score']
            await message.answer(f'К сожалению ты проиграл😢\n\nТвой счет {user_score}') #\n\nТвой счет {user_score}
            users_db[message.from_user.id]['score'] = 0
            users_db[message.from_user.id]['life'] = 3
            await state.clear()
            await message.answer(text = 'Если захожешь играть то жмякни на кнопку\n<b><i>Жмякни если хочешь играть!😍</i></b>\n\n\nПримечание: <i><u>Теперь вы можете использовать стандартные функции</u></i>', reply_markup=start_mr)
            
        #     # Save data to database
        # conn = sqlite3.connect('users.db')
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO users (user_id, score, life) VALUES (?, ?, ?)", 
        #                (message.from_user.id, user_score, user_life))
        # conn.commit()
        # conn.close()


@router.message(F.text == 'Я хочу играть до победного😈', StateFilter(FSMgame.yes_no_game))
async def game(message: Message, state: FSMContext):
    global bot_otv
    await message.answer(f'Вот твое слово, переведи его🗿\n\n                   <b>{bot_otv}</b>')
    await state.set_state(FSMgame.vvod_word)


@router.message(F.text.in_(['Я не хочу играть🥲']), StateFilter(FSMgame.yes_no_game))
async def no_game(message: Message, state: FSMContext):
    await message.answer(text = 'Если захожешь играть то жмякни на кнопку\n<b><i>Жмякни если хочешь играть!😍</i></b>\n\n\nПримечание: <i><u>Теперь вы можете использовать стандартные функции</u></i>', reply_markup=start_mr)
    await state.clear()
    users_db[message.from_user.id]['score'] = 0
    users_db[message.from_user.id]['life'] = 3