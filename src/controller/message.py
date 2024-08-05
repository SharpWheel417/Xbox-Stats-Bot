import subprocess
import os
from telegram import Game, Update, Bot
from telegram.ext import CallbackContext, ContextTypes
import subprocess

from config import ADMIN_ID
from src.model.users import User
from ..view.send import send_pic, sendmess, sendmess_buttons

from ..parsing import openxbl as xbox
from src.model.games import Game

from src.model.achivment import Achievement

import src.view.buttons as buttons

# TODO
# terminal = subprocess.Popen(['gnome-terminal'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

async def handle_message(update: Update, context: CallbackContext):

    text = update.message.text

    u = User('', update.effective_user.id, '', '', '').get()

    if u.stage == 'get_xapi':
        u.xapi = text
        u.stage = 'home'
        u.set_xapi()
        u.set_stage()
        await sendmess('API key installed', update, context)
        return

    if u.stage == 'home':

        if text == 'Send API key':
            u.stage = 'get_xapi'
            u.set_stage()
            await sendmess('Paste API key and send', update, context)
            return

        if text == 'Update games':
            xbox.update_games(u.get_id(), u.xapi)
            games = Game(u.get_id()[0], '', '').get_all()
            txt=''
            for game in games:
                txt+=f'{game.name}\n'

            await sendmess(txt, update, context)

        if text == 'Achivment':
            games = Game(u.get_id()[0], '', '').get_all()
            u.stage = 'change_games_achivments'
            u.set_stage()
            await sendmess_buttons("Change game", buttons.game_page(games), update, context)
            return

        if text == 'Media':
            media = xbox.get_sceenshots(u.xapi)
            for m in media:
                if m.type == 'video':
                    await send_pic(m.screen_url, f'{m.video_url}',  update, context)
                elif m.type == 'photo':
                    await send_pic(m.screen_url, "", update, context)

        if text == 'Achivment list':
            games = Game(u.get_id()[0], '', '').get_all()
            u.stage = 'change_games_achivments_list'
            u.set_stage()
            await sendmess_buttons("Change game", buttons.game_page(games), update, context)
            return

        if text == 'Time':
            games = Game(u.get_id()[0], '', '').get_all()
            u.stage = 'change_games_time'
            u.set_stage()
            await sendmess_buttons("Change game", buttons.game_page(games), update, context)
            return

    if u.stage == 'change_games_time':
        game = Game(u.get_id()[0], text, '')
        game_id = game.get_game_id()
        time = xbox.get_minuted_playes(u.xapi, game_id)
        u.stage='home'
        u.set_stage()
        await sendmess(str(time), update, context, reply_markup=buttons.user_base)
        return

    ## СПИСОК АЧИВОК
    if u.stage == 'change_games_achivments_list':
        game = Game(u.get_id()[0], text, '')
        game_id = game.get_game_id()
        achivments = xbox.get_achivments(game_id, u.xapi)
        u.stage='home'
        u.set_stage()
        i=0
        messages = []
        for achivment in achivments:
            if achivment.progressState == 'Achieved':
                messages.append(f'✅{achivment.name}')
            else:
                messages.append(f'❌{achivment.name}')
        if messages:
            await split_message_send(messages=messages, update=update, context=context)


    ## ВЫБОР ИГРЫ ДЛЯ АЧИВОК
    if u.stage == 'change_games_achivments':
        u.stage = 'change_sort_achivments'
        u.set_stage()
        u.pick_game = text
        u.set_pick_game()
        await sendmess_buttons("Change sort", buttons.achivment_sort, update, context)
        return

    ## ВЫБОР СОРТИРОВКИ АЧИВОК
    if u.stage == 'change_sort_achivments':
        game = Game(u.get_id()[0], u.pick_game, '')
        game_id = game.get_game_id()
        achivments = xbox.get_achivments(game_id, u.xapi)
        u.stage='home'
        u.set_stage()
        await switch_send_ach(type=text, achivments=achivments, update=update, context=context)



    ## ВЫБОР ИГРЫ
    if u.stage == 'change_games':
        game = Game(u.get_id()[0], text, '')
        game_id = game.get_game_id()
        achivments = xbox.get_achivments(game_id, u.xapi)
        i=0
        messages = []
        for achivment in achivments:
            if achivment.progressState == 'Achieved':
                continue
            if i > 5:
                # Append the achievement text to the messages list
                messages.append(f'{achivment.name}\n{achivment.description}\isSecret: {achivment.isSecret}\progressState: {achivment.progressState}\nG:{achivment.value}')
            else:
                # Display the achievement with image
                await send_pic(f=achivment.iconURL, text=f'{achivment.name}\n{achivment.description}\isSecret: {achivment.isSecret}\progressState: {achivment.progressState}\nG:{achivment.value}', update=update, context=context)
            i+=1
        if messages:
            # Split the messages into chunks of 2000 characters
            message_chunks = [messages[i:i+255] for i in range(0, len(messages), 255)]

            # Send each chunk as a separate message
            for i, chunk in enumerate(message_chunks):
                await sendmess('\n'.join(chunk), update=update, context=context)








    if text == 'Account':
        account = xbox.get_acc()
        await send_pic(account.GemrIconUrl, f'Tag: {account.GamerTag}\nScore: {account.GamerScore}', update, context)





async def switch_send_ach(type, achivments, update: Update, context: ContextTypes):
    '''
        Сортирует и выводит ачивки
    '''

    i=0
    messages = []
    for achivment in achivments:
            if type == 'Unfulfilled':
                if achivment.progressState == 'Achieved':
                    continue
            if type == 'Started':
                if achivment.progressState == 'NotStarted' or achivment.progressState == 'Achieved':
                    continue
            if i > 5:
                messages.append(f'{achivment.name}\n{achivment.description}\nСекретное: {achivment.isSecret}\nПрогресс: {achivment.progressState}\nG:{achivment.value}')
            else:

                await send_pic(f=achivment.iconURL, text=f'{achivment.name}\n{achivment.description}\nСекретное: {achivment.isSecret}\nПрогресс: {achivment.progressState}\nG:{achivment.value}', update=update, context=context)
            i+=1


    if messages:
            message_chunks = [messages[i:i+220] for i in range(0, len(messages), 220)]

            for i, chunk in enumerate(message_chunks):
                await sendmess('\n'.join(chunk), update=update, context=context, reply_markup=buttons.user_base)



async def split_message_send(messages, update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
        Разбивает массивное сообщение и отправляет польщователю
    '''
    # Split the messages into chunks of 255 characters
    message_chunks = [messages[i:i+255] for i in range(0, len(messages), 255)]
    for i, chunk in enumerate(message_chunks):
        await sendmess('\n'.join(chunk), update=update, context=context, reply_markup=buttons.user_base)
