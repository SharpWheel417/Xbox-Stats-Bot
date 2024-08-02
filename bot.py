from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, CallbackContext, filters

from config import BOT_TOKEN

from src.parsing.openxbl import get_acc



from src.controller.message import handle_message
import src.controller.command as command

application = ApplicationBuilder().token(BOT_TOKEN).build()

# application.add_handler(CallbackQueryHandler(button_callback))


### COMMAND
start_handler = CommandHandler('start', command.start)
application.add_handler(start_handler)

### TEXT
message_handler = MessageHandler(filters.TEXT, handle_message)
application.add_handler(message_handler)

application.run_polling()