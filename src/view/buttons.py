from telegram import ReplyKeyboardMarkup

from src.model.games import Game

user_base = ReplyKeyboardMarkup([['Ачивки', 'Медиа', 'Аккаунт'], ['Ввести ключ OpenXBL', 'Обновить игры', 'Аккаунт', 'Games'], ['Помощь']], resize_keyboard=True)

def game_page(games: Game):
    mass_buttons = []
    for game in games:
        mass_buttons.append([game.name])

    return ReplyKeyboardMarkup(mass_buttons, resize_keyboard=True)