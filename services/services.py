import random

from lexicon.lexicon import LEXICON_MAIN, LEXICON_LENG, LEXICON_RU


#функция для случайного слова
def random_word():
    return random.choice(LEXICON_MAIN)



#функция для сравнивания ответа пользователя с ключом 
def check_answer(user_otv: str, bot_otv: str) -> str:
    bot_perevod = LEXICON_LENG[bot_otv]
    if user_otv == bot_perevod:
        return LEXICON_RU['prav_otv']
    else:
        return LEXICON_RU['neprav_otv']