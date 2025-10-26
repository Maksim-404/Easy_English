import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart

# Я импортирую все необходимые компоненты из других файлов
from config import TOKEN, init_db, user_states
from handlers import (
    start_command, handle_name_input, handle_level_selection,
    mark_word_learned, next_word, finish_learning
)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Я регистрирую обработчики сообщений с фильтрами
dp.message.register(start_command, CommandStart())
# Я проверяю что пользователь в состоянии ожидания имени
dp.message.register(handle_name_input, F.text, lambda message: message.from_user.id in user_states and user_states[message.from_user.id] == 'waiting_name')
# Я проверяю что пользователь в состоянии ожидания уровня
dp.message.register(handle_level_selection, F.text, lambda message: message.from_user.id in user_states and user_states[message.from_user.id] == 'waiting_level')

# Я обрабатываю конкретные текстовые команды от кнопок
dp.message.register(mark_word_learned, F.text == '✅ Выучил')
dp.message.register(next_word, F.text == '⏭️ Следующее')
dp.message.register(finish_learning, F.text == '🔚 Завершить')



# Я создаю главную асинхронную функцию для запуска бота
async def main():
    init_db()
    print('🚀 Easy English запущен и готов к работе!')
    try:
        await dp.start_polling(bot) 
    except KeyboardInterrupt:
        print('\n🛑 Easy English остановлен пользователем.')
    except Exception as e:
        print(f'\n❌ Произошла ошибка: {e}')
    finally:
        # Я закрываю сессию бота при завершении работы
        await bot.session.close()
        print('👋 До скорой встречи!')

if __name__ == '__main__':
    try:
        # Я запускаю асинхронную главную функцию
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n🛑 Бот остановлен.')
        