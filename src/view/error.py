from telegram import Update
from telegram.ext import ContextTypes

### Комманда Старт ###
async def error_mess(text, update: Update, context: ContextTypes.DEFAULT_TYPE):

    if text == 'File is too big':
        text = 'Ошика. \n файл слижком большой!'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(text))