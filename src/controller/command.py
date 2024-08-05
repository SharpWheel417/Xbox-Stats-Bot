from telegram import Update
from telegram.ext import ContextTypes

from src.model import users

import src.view.buttons as buttons

import config as config

### Комманда Старт ###
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

  u = users.User(update.effective_user.full_name, update.effective_chat.id, 'home', '', '')

  u.add()

  await context.bot.send_message(chat_id=update.effective_chat.id, text="Кароче этот бот ковертирует:\n\ndoc,docx -> pdf\n\nСжимает html, css, js\n\nПросто скинь нужный файл, а он вернет тебе обработанный\n\nУдачи!", reply_markup=buttons.user_base)