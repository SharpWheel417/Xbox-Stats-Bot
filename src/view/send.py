from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_TOKEN
import requests
import telegram

async def sendmess(text: any, update: Update, context: ContextTypes):
  await context.bot.send_message(chat_id=update.effective_chat.id, text=str(text), parse_mode='Markdown')


async def sendmess_buttons(text: any, reply_markup: any, update: Update, context: ContextTypes):
  await context.bot.send_message(chat_id=update.effective_chat.id, text=str(text), parse_mode='Markdown', reply_markup=reply_markup)


async def send_pic(f: any, text: any, update: Update, context: ContextTypes):
  await context.bot.send_photo(chat_id=update.effective_chat.id, photo=f, caption=str(text))

def sendmess_user_id(txt, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={txt}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}\n{response.text}")


def sendmess_chat_id(txt, chat_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id=-{chat_id}&text={txt}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message. Status code: {response.status_code}\n{response.text}")