import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError('BOT_TOKEN не найден в .env файле!')

user_states = {}

# Я создал словари слов для трех уровней сложности
WORD_SETS = {
    '🌱 Начальный': {
        'words': [
            {'english': 'hello', 'russian': 'привет'},
            {'english': 'house', 'russian': 'дом'},
            {'english': 'book', 'russian': 'книга'},
            {'english': 'water', 'russian': 'вода'},
            {'english': 'friend', 'russian': 'друг'},
            {'english': 'school', 'russian': 'школа'},
            {'english': 'family', 'russian': 'семья'},
            {'english': 'city', 'russian': 'город'},
            {'english': 'food', 'russian': 'еда'},
            {'english': 'time', 'russian': 'время'}
        ]
    },
    '🎯 Средний': {
        'words': [
            {'english': 'environment', 'russian': 'окружающая среда'},
            {'english': 'knowledge', 'russian': 'знание'},
            {'english': 'opportunity', 'russian': 'возможность'},
            {'english': 'development', 'russian': 'развитие'},
            {'english': 'technology', 'russian': 'технология'},
            {'english': 'education', 'russian': 'образование'},
            {'english': 'government', 'russian': 'правительство'},
            {'english': 'population', 'russian': 'население'},
            {'english': 'experience', 'russian': 'опыт'},
            {'english': 'information', 'russian': 'информация'}
        ]
    },
    '🚀 Профи': {
        'words': [
            {'english': 'accommodate', 'russian': 'приспосабливать'},
            {'english': 'benevolent', 'russian': 'благожелательный'},
            {'english': 'connoisseur', 'russian': 'знаток'},
            {'english': 'diligent', 'russian': 'усердный'},
            {'english': 'ephemeral', 'russian': 'мимолетный'},
            {'english': 'fastidious', 'russian': 'привередливый'},
            {'english': 'gregarious', 'russian': 'общительный'},
            {'english': 'hierarchy', 'russian': 'иерархия'},
            {'english': 'idiosyncrasy', 'russian': 'особенность'},
            {'english': 'juxtaposition', 'russian': 'сопоставление'}
        ]
    }
}

def init_db():
    # Я создаю базу данных и таблицу для пользователей
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            level TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id: int):
    # Я ищу пользователя в базе данных по его ID
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(user_id: int, name: str):
    # Я создаю нового пользователя в базе данных
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    conn.close()

def update_user_name(user_id: int, name: str):
    # Я обновляю имя пользователя в базе данных
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = ? WHERE user_id = ?', (name, user_id))
    conn.commit()
    conn.close()

def update_user_level(user_id: int, level: str):
    # Я обновляю уровень пользователя в базе данных
    conn = sqlite3.connect('english_bot.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET level = ? WHERE user_id = ?', (level, user_id))
    conn.commit()
    conn.close()
    