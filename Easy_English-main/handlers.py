from aiogram import types, F
from aiogram.types import Message
from aiogram.filters import CommandStart

# Я импортирую все необходимые данные и функции из config.py
from config import user_states, WORD_SETS
from config import get_user, create_user, update_user_name, update_user_level

async def start_learning_session(message: Message, level: str):
    # Я начинаю сессию обучения для пользователя
    user_id = message.from_user.id
    words = WORD_SETS[level]['words']
    
    # Я создаю состояние пользователя для отслеживания прогресса
    user_states[user_id] = {
        'mode': 'learning_words',
        'level': level,
        'current_word_index': 0,
        'words_learned': 0
    }
    
    await show_current_word(message, user_id)

async def show_current_word(message: Message, user_id: int):
    # Я показываю текущее слово пользователю
    user_state = user_states[user_id]
    word_index = user_state['current_word_index']
    words = WORD_SETS[user_state['level']]['words']
    current_word = words[word_index]
    
    # Я создаю клавиатуру с кнопками для управления обучением
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='✅ Выучил')],
            [types.KeyboardButton(text='⏭️ Следующее')],
            [types.KeyboardButton(text='🔚 Завершить')]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f'📖 Слово {word_index + 1} из {len(words)}\n\n'
        f'🇬🇧 <b>{current_word["english"]}</b>\n'
        f'🇷🇺 {current_word["russian"]}',
        reply_markup=keyboard,
        parse_mode='HTML'
    )

async def finish_session(message: Message, user_state: dict, words: list, completed: bool):
    # Я завершаю сессию обучения и показываю результаты
    user_id = message.from_user.id
    
    if completed:
        text = f'🎉 Поздравляю! Ты выучил все {len(words)} слов!\n'
    else:
        text = '🏁 Обучение завершено!\n'
    
    text += f'📊 Выучено слов: {user_state["words_learned"]}/{len(words)}'
    
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    user_states[user_id] = 'ready'

# Я создаю обработчик для команды /start
async def start_command(message: Message):
    user_states[message.from_user.id] = 'waiting_name'
    welcome_text = (
        '👋 Привет! Я — Easy English, твой личный бот для изучения английского языка 🇬🇧\n\n'
        '📚 Я помогу тебе улучшить английский с любого уровня!\n\n'
        'Как тебя зовут?'
    )
    remove_keyboard = types.ReplyKeyboardRemove()
    await message.answer(welcome_text, reply_markup=remove_keyboard, parse_mode='HTML')

# Я обрабатываю ввод имени пользователя
async def handle_name_input(message: Message):
    user_id = message.from_user.id
    user_name = message.text.strip()
    
    # Я проверяю что имя состоит только из букв
    if not user_name.replace(' ', '').isalpha():
        await message.answer('Пожалуйста, введи имя только буквами, без цифр и символов')
        return
    
    if len(user_name) < 2:
        await message.answer('Пожалуйста, введи настоящее имя (минимум 2 буквы)')
        return
    
    # Я сохраняю пользователя в базу данных
    existing_user = get_user(user_id)
    if existing_user:
        update_user_name(user_id, user_name)
    else:
        create_user(user_id, user_name)
    
    user_states[user_id] = 'waiting_level'
    
    # Я создаю клавиатуру для выбора уровня
    levels_keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='🌱 Начальный')],
            [types.KeyboardButton(text='🎯 Средний')],
            [types.KeyboardButton(text='🚀 Профи')]
        ],
        resize_keyboard=True
    )
    
    await message.answer(
        f'Приятно познакомиться, {user_name}! 🎉\n\n'
        'Теперь выбери свой уровень английского:',
        reply_markup=levels_keyboard
    )

# Я обрабатываю выбор уровня пользователем
async def handle_level_selection(message: Message):
    user_id = message.from_user.id
    level = message.text
    
    # Я проверяю что выбран корректный уровень
    if level not in WORD_SETS:
        await message.answer('Пожалуйста, выбери уровень из предложенных вариантов')
        return
    
    update_user_level(user_id, level)
    await start_learning_session(message, level)

# Я обрабатываю кнопку "Выучил"
async def mark_word_learned(message: Message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id)
    
    # Я проверяю что пользователь в режиме изучения слов
    if isinstance(user_state, dict) and user_state.get('mode') == 'learning_words':
        user_state['words_learned'] += 1
        user_state['current_word_index'] += 1
        words = WORD_SETS[user_state['level']]['words']
        
        if user_state['current_word_index'] >= len(words):
            await finish_session(message, user_state, words, True)
        else:
            await show_current_word(message, user_id)

# Я обрабатываю кнопку "Следующее"
async def next_word(message: Message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id)
    
    if isinstance(user_state, dict) and user_state.get('mode') == 'learning_words':
        user_state['current_word_index'] += 1
        words = WORD_SETS[user_state['level']]['words']
        
        if user_state['current_word_index'] >= len(words):
            await finish_session(message, user_state, words, False)
        else:
            await show_current_word(message, user_id)

# Я обрабатываю кнопку "Завершить"
async def finish_learning(message: Message):
    user_id = message.from_user.id
    user_state = user_states.get(user_id)
    
    if isinstance(user_state, dict) and user_state.get('mode') == 'learning_words':
        words = WORD_SETS[user_state['level']]['words']
        await finish_session(message, user_state, words, False)
        