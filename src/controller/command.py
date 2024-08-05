from telegram import Update
from telegram.ext import ContextTypes

from src.model import users

import src.view.buttons as buttons

import config as config

### Комманда Старт ###
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

  u = users.User(update.effective_user.full_name, update.effective_chat.id, 'home', '', '')

  u.add()

  await context.bot.send_message(chat_id=update.effective_chat.id, text='''This bot displays your XBOX account statistics.\n\nFirst, you need to register on this site: https://xbl.io Then, on the profile tab, create an API key and copy it.
\n\nNext, click the "Send API key" button in the bot. Then send the key to the bot.
\n\nAfter that, click the "Update game list" button. \nAfter that, the bot will display a list of your games where progress already exists.
\n\nDone! Now you have access to the full functionality of the bot''', reply_markup=buttons.user_base)