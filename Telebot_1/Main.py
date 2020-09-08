import database_commands
import time
import asyncio
import logging
import contextvars
import random

from config import token
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
database_commands.create_table()
database_commands.add_users()
database_commands.add_cameras()

# для антиспама // сколько сообщений отправил бот 
# number_of_messages = contextvars.ContextVar(0)

#________________________________________________________________________________________
# начало обработки реакции на комманды

@dp.message_handler(commands = ['start'])
async def statring(message: types.Message):
    await message.answer(standart_text(message.from_user.id))
    

# подписаться 
@dp.message_handler(commands = ['sub'])
async def sub(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "sub")
        await message.answer("Введите номер камеры на которую хотите подписаться")
    else:
        await message.answer(text_report_lack_of_right())
    
        
# отписаться
@dp.message_handler(commands = ['stop'])
async def stop(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "stop")
        await message.answer("Введите номер камеры откоторой хотите отписаться или 'all' для отмены всех подписок")
    else:
        await message.answer(text_report_lack_of_right())
    
# инфа о подписках
@dp.message_handler(commands = ['cameras'])
async def cameras(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "calmness")
        await message.answer(database_commands.cameras(message.from_user.id) + f"\n\n" + standart_text(message.from_user.id))
    else:
        await message.answer(text_report_lack_of_right())

 

# информация о всех камерах
@dp.message_handler(commands = ['get_info'])
async def get_info(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "calmness")
        await message.answer(database_commands.get_info() + f"\n\n" + standart_text(message.from_user.id))
    else:  
        await message.answer(text_report_lack_of_right())
    

#______________________________________________________________________________________________
# симуляция получения события если не нужно будет то удалить к ****
@dp.message_handler(commands = ['get_camera_info'])
async def get_camera_info(message: types.Message):
    for i in range(1,1000):
        await reaction_to_event(1, 'image1.jpg', 'пример текста1')
        await reaction_to_event(3, 'image3.jpg', 'пример текста3')
        await reaction_to_event(4, 'image4.jpg', 'пример текста4')
    await message.answer("конец проверки")


@dp.message_handler(commands = ['get_camera_info1'])
async def get_camera_info(message: types.Message):
    await reaction_to_event(1, 'image1.jpg', "пример текста1")
    await message.answer("конец проверки")


@dp.message_handler(commands = ['get_camera_info3'])
async def get_camera_info(message: types.Message):
    await reaction_to_event(3, 'image3.jpg', 'пример текста3')
    await message.answer("конец проверки")


@dp.message_handler(commands = ['get_camera_info4'])
async def get_camera_info(message: types.Message):
    await reaction_to_event(4, 'image4.jpg', 'пример текста4')
    await message.answer("конец проверки")
# конец симуляции
#________________________________________________________________________________________


# конец обработки реакции на комманды
#________________________________________________________________________________________

@dp.message_handler(content_types=["text"])
async def any_not_command_message(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        status = database_commands.get_status_user(message.from_user.id)
        if status[0] == "sub":
            await message.answer(database_commands.sub(message.from_user.id, message.text))
        elif status[0] == "stop":
            await message.answer(database_commands.stop(message.from_user.id, message.text)) 
        database_commands.change_status_user(message.from_user.id, "calmness") # эта строчка служит защитой от ситуаций случайных отписок/подписок, а лучше с ней или без нее не моего ума дело
        await message.answer(standart_text(message.from_user.id))
    else:
        await message.answer(standart_text(message.from_user.id))


# без понятия как это описать лучше чем это делает название
async def reaction_to_event(camera_id, image, text):
    with open(image, 'rb') as photo:
        for value in database_commands.who_subscribed_to_the_camera(camera_id):
            database_commands.change_the_number_of_sent_messages('add')
            if not (database_commands.is_it_possible_to_send_another_message_to_the_user()):
                print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
                time.sleep(1.2)     # не меньше 1
                database_commands.change_the_number_of_sent_messages()
            time.sleep(0.1)         # можно поэксперементировать
            print("qweakkka")
            await bot.send_photo(value[0], photo, text)

# что отправлять на старте или если сообщение - не комманда
def standart_text(id):
    if database_commands.does_the_user_have_access(id):
        return text_instructions()
    else:
        return text_report_lack_of_right()


# инструкции к боту
def text_instructions():
    return """Вы можете управлять мной, отправляя эти команды: 
/sub - выбор камеры для подписки.
/stop - отменить подписку на камеру.
/cameras - список камер, на которые вы подписаны.
/get_info - получить информацию о всех камерах.
/get_camera_info - симулирует получение события на каждую камеру
/get_camera_info1 - симулирует получение события на 1 камеру
/get_camera_info3 - симулирует получение события на 3 камеру
/get_camera_info4 - симулирует получение события на 4 камеру"""

def text_report_lack_of_right():
    return "Извините, Вам не разрешен доступ к функционалу этого бота"


if __name__ == '__main__':    
    executor.start_polling(dp, skip_updates=True) 
    