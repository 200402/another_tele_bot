import telebot 
import database_commands

bot = telebot.TeleBot('1246495184:AAHTb5Syjr3PctV6ROOg_yMiMyvodDbmvXI')
database_commands.create_table()
database_commands.add_users()
database_commands.add_cameras()

#________________________________________________________________________________________
# начало обработки реакции на комманды

@bot.message_handler(commands = ['start'])
def statring(message):
    bot.send_message(message.chat.id, standart_text)
    

# подписаться
@bot.message_handler(commands = ['sub'])
def sub(message):
    if database_commands.does_the_user_have_access(message.chat.id):
        database_commands.change_status_user(message.chat.id, "sub")
        bot.send_message(message.chat.id, "Введите номер камеры на которую хотите подписаться")
    
        
# отписаться
@bot.message_handler(commands = ['stop'])
def sub(message):
    if database_commands.does_the_user_have_access(message.chat.id):
        database_commands.change_status_user(message.chat.id, "stop")
        bot.send_message(message.chat.id, "Введите номер камеры откоторой хотите отписаться или 'all' для отмены всех подписок")
    
# инфа о подписках
@bot.message_handler(commands = ['cameras'])
def sub(message):
    if database_commands.does_the_user_have_access(message.chat.id):
        database_commands.change_status_user(message.chat.id, "cameras")
        pass ############################################################################
 

# т.к. я хз как и какая приходит информация с камер, я решил поставить эту заглушку
@bot.message_handler(commands = ['get_info'])
def sub(message):
    if database_commands.does_the_user_have_access(message.chat.id):
        pass

# конец обработки реакции на комманды
#________________________________________________________________________________________

@bot.message_handler(content_types=["text"])
def any_not_command_message(message):
    if database_commands.does_the_user_have_access(message.chat.id):
        status = database_commands.get_status_user(message.chat.id)
        if status[0] == "sub":
            bot.send_message(message.chat.id, database_commands.sub(message.chat.id, message.chat.text))
        elif status[0] == "stop":
            pass
        elif status[0] == "cameras":
            pass
        database_commands.change_status_user(message.chat.id, "calmness") 
        # пока, что так, но если нужно работать с множеством камер, то надо переделать
        # поправлю или сделаю красивее пофсле получения правок
    bot.send_message(message.chat.id, standart_text)


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
/get_info - получить всю скопившуюся информацию с камер."""

def text_report_lack_of_right():
    return "Извините, Вам не разрешен доступ к функционалу этого бота"



bot.polling(none_stop=True)