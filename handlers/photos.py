from config import bot

def photo_message_handle(message):
    cid = message.chat.id
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    download_file = bot.download_file(file_path=file_info.file_path)
    filename = f'{cid}_photo.jpg'
    with open(filename, 'wb') as f:
        f.write(download_file)
    print(f'Photo saved as {filename}')
