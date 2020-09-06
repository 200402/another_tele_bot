import database_commands
from config import token

from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token)
dp = Dispatcher(bot)
database_commands.create_table()
database_commands.add_users()
database_commands.add_cameras()

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
    
        
# отписаться
@dp.message_handler(commands = ['stop'])
async def stop(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "stop")
        await message.answer("Введите номер камеры откоторой хотите отписаться или 'all' для отмены всех подписок")
    
# инфа о подписках
@dp.message_handler(commands = ['cameras'])
async def cameras(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "calmness")
        await message.answer(database_commands.cameras(message.from_user.id) + f"\n\n" + standart_text(message.from_user.id))
 

# информация о всех камерах
@dp.message_handler(commands = ['get_info'])
async def get_info(message: types.Message):
    if database_commands.does_the_user_have_access(message.from_user.id):
        database_commands.change_status_user(message.from_user.id, "calmness")
        await message.answer(database_commands.get_info() + f"\n\n" + standart_text(message.from_user.id))

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
        database_commands.change_status_user(message.from_user.id, "calmness") 
        # мне это не нравися; это не удобно, если камер много, да и по 2 сообщения за раз присылает, но как защита от косяков пока что сойдет
    await message.answer(standart_text(message.from_user.id))


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
/get_info - получить информацию о всех камерах."""

def text_report_lack_of_right():
    return "Извините, Вам не разрешен доступ к функционалу этого бота"


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)