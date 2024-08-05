from telegram import ReplyKeyboardMarkup

from src.model.games import Game

user_base = ReplyKeyboardMarkup([['Media', 'Account'], ['Achivment', 'Achivment list', 'Time'], ['Send API key', 'Update games']], resize_keyboard=True)

achivment_sort = ReplyKeyboardMarkup([['All', 'Unfulfilled'], ['Started']], resize_keyboard=True)

def game_page(games: Game):
    mass_buttons = []
    for game in games:
        mass_buttons.append([game.name])

    return ReplyKeyboardMarkup(mass_buttons, resize_keyboard=True)
