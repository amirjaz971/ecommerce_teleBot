from config import bot


def command_default(message):
    cid = message.chat.id
    bot.send_message(cid, 'Invalid command. Use /help to see the list of available commands.')