"""
Terminal TG
Version 0.1.7
"""

from telethon import TelegramClient, events
from datetime import datetime

try:
    with open('config', 'r') as f:
        lines = f.readlines()
        if len(lines) >= 2:
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
        else:
            print("config does not have enough lines.")
            sys. exit()
except FileNotFoundError:
    print("config not found.")
    sys. exit()

client = TelegramClient('terminal_telegram', api_id, api_hash)

#система уведомлений изначально выключина
yv = False

@client.on(events.NewMessage())
async def my_event_handler(event):
    if yv:
        if event.is_private:
           # Пользователь общается в личном чате
           name = event.chat.first_name
        else:
           # Сообщение отправлено из группового чата или канала
           if hasattr(event.chat, 'title'):
               name = event.chat.title
           else:
                name = 'Unnamed chat'

        message = event.message.message

        time = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # получаем дату и время

        # выводим данные
        print(f"Name: {name} | Message: {message} | Time: {time}")

#основная часть
async def main():
    await client.start()
    print('Client started')
    async with client:
        while True:
            print("\nTerminal TG\nVersion: 0.1.7\nCommands:\nchats\nhistory chat\nsearch cha\nsend name message\nsd -p chat photo\nsd -f chat file\nexit")
            user_input = input('Enter command: ')
            print("\n")
            if user_input == 'chats':
                async for dialog in client.iter_dialogs():
                    print(dialog.name)
            elif user_input.startswith('history'):
                chat_id = ' '.join(user_input.split(' ')[1:])
                async for message in client.iter_messages(chat_id, limit=10):
                    event = message
                    if event.is_private:
                         # Пользователь общается в личном чате
                        name = event.chat.first_name
                    else:
                        # Сообщение отправлено из группового чата или канала
                        if hasattr(event.chat, 'title'):
                           name = event.chat.title
                        else:
                            name = 'Unnamed chat'
                    print(f"Name: {name} | Message: {message.text} | Date: {message.date}")
            elif user_input.startswith('search'):
                chat_s = user_input.split(' ')[1]
                async for dialog in client.iter_dialogs():
                   if chat_s in dialog.name:
                      print("found(name): " + dialog.name)
                   if hasattr(dialog.entity, 'username') and dialog.entity.username is not None and dialog.entity.username != "":
                      if chat_s in dialog.entity.username:
                         print("found(username): " + dialog.entity.username)
            elif user_input.startswith('send'):
                user_to_send = user_input.split(' ')[1]
                message_to_send = ' '.join(user_input.split(' ')[2:])
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # получаем дату и время
                print(f"To: {user_to_send} | Message: {message_to_send} | Date: {date}")
                await client.send_message(user_to_send, message_to_send)
            elif user_input.startswith('sd'):
               fp = user_input.split(' ')[1]
               if fp == "-p":
                   user_to_send = user_input.split(' ')[2]
                   file_path = user_input.split(' ')[3]
                   date = datetime.now().strftime("%d/%m/%Y %H:%M:%S") # ???????????????? ???????? ?? ??????????
                   print(f"To: {user_to_send} | Photo path: {file_path} | Date: {date}")
                   await client.send_file(user_to_send, file_path)
               if fp == "-f":
                   user_to_send = user_input.split(' ')[2]
                   file_path = user_input.split(' ')[3]
                   date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                   print(f"To: {user_to_send} | File path: {file_path} | Date: {date}")
                   await client.send_file(user_to_send, file_path)

            elif user_input == 'exit':
                break
            else:
                print('Invalid command') 

if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print('Bot has been stopped')
    finally:
        client.disconnect()
