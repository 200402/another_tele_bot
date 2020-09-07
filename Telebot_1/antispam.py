import database_commands
import multiprocessing
import time

# файл моего позора, не буду удалять авось кто то доведет до ума

number_of_messages = multiprocessing.Value('i', 0)

# задерживает выполнение программы пока не будут выполняться условия антиспама
def antispamer(user_id):
    while (database_commands.is_it_possible_to_send_another_message_to_the_user(user_id)):
        time.sleep(0.1)
    while number_of_messages.value > 30:
        time.sleep(0.1)
    change_the_number_of_messages_sent_by_the_bot()
    change_the_number_of_messages_sent_by_the_bot_to_the_user(user_id)
    


# изменить количество сообщений отправленных ботом за последние {second} секунд
def change_the_number_of_messages_sent_by_the_bot():
    print("1")
    number_of_messages.value += 1
    second = 1.2
    time.sleep(second)
    number_of_messages.value -= 1
    print("11")


# изменить количество сообщений отправленных ботом конкретному пользователю за последние {second} секунд
def change_the_number_of_messages_sent_by_the_bot_to_the_user(user_id):
    print("2")
    database_commands.change_the_number_of_sent_messages(user_id, "add")
    second = 1
    time.sleep(second)
    database_commands.change_the_number_of_sent_messages(user_id, "lower")
    print("22")


# конец система антиспама
#________________________________________________________________________________________
