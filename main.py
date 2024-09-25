import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.menu import set_main_menu

from middlewares.throtling import ThrottlingMiddleware

logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main() -> None:
    #log
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    #меню бота 
    await set_main_menu(bot)

    #подрубаем роутеры
    dp.include_routers(
        user_handlers.router,
        other_handlers.router,
    )

    #middleware
    # dp.update.middleware(ThrottlingMiddleware())

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=[])

if __name__ == '__main__':
    asyncio.run(main())
