import sqlite3

#db = sqlite3.connect("mydatabase.db")
#sql = db.cursor()

# если использвать глобальные переменные то выбает эту ошибку:
# SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 11340 and this is thread id : 12924
# если есть более изящный способ решить эту проблему, то я бы с удовольствием о нем узнал


# создание таблиц
def create_table():
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    sql.execute("""PRAGMA foreign_keys=on""")

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY, 
                status TEXT
                )""") 

    sql.execute("""CREATE TABLE IF NOT EXISTS cameras (
                id TEXT PRIMARY KEY,
                description TEXT
                )""") 

    sql.execute("""CREATE TABLE IF NOT EXISTS users_cameras (
                users_id TEXT NOT NULL,
                cameras_id TEXT NOT NULL,
                FOREIGN KEY (users_id) REFERENCES users(id)
                FOREIGN KEY (cameras_id) REFERENCES cameras(id)
                )""")
    db.commit()
    db.close()

# добавление юзеров
def add_users():
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    users_id = ['454054254', "123212", "12312212"]
    for user_id in users_id:
        sql.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?,?)", (user_id,"calmness",))
    db.commit()
    db.close()

# добавление камер
def add_cameras():
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    cameras_id = ['1', "3", "4"]
    for camera_id in cameras_id:
        sql.execute(f"SELECT id FROM cameras WHERE id = '{camera_id}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO cameras VALUES (?,?)", (camera_id,"инфа о камере",))
    db.commit()
    db.close()

# есть ли у юзера доступ к боту
def does_the_user_have_access(id):
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    sql.execute(f"SELECT id FROM users WHERE id = '{id}'")
    if sql.fetchone() is None: 
        db.close()
        return False
    else:
        db.close()
        return True

# команда sub
def sub(id_user, id_camera):
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    sql.execute(f"SELECT * FROM cameras WHERE id = '{id_camera}'")
    if sql.fetchone() is None:
        db.close()
        return "Нет камеры с таким номером"
    else:
        sql.execute(f"SELECT * FROM users_cameras WHERE users_id = '{id_user}' AND cameras_id = '{id_camera}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users_cameras VALUES (?,?)", (id_user, id_camera,))
            db.commit()
            db.close()
            return f"Вы успешно подписались на камеру с номером {id_camera}"
        else:
            db.close()
            return f"Вы уже подписаны на камеру с номером {id_camera}"


# команда stop
def stop(id_user, id_camera):
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    sql.execute(f"SELECT * FROM cameras WHERE id = '{id_camera}'")
    if id_camera.lower() == "all":
        sql.execute(f"DELETE FROM users_cameras WHERE users_id = '{id_user}'")
        db.commit()
        db.close()
        return "Вы отменили все свои подписки"
    elif sql.fetchone() is None:
        db.close()
        return "Нет камеры с таким номером"
    else:
        sql.execute(f"SELECT * FROM users_cameras WHERE users_id = '{id_user}' AND cameras_id = '{id_camera}'")
        if sql.fetchone() is None:
            db.close()
            return f"Вы не были подписаны на камеру с номером {id_camera}"
        else:
            sql.execute(f"DELETE FROM users_cameras WHERE users_id = '{id_user}' AND cameras_id = '{id_camera}'")
            db.commit()
            db.close()
            return f"Вы отменили подписку на камеру с номером {id_camera}"


# команда cameras
def cameras(id_user):
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    sql.execute(f"SELECT * FROM users_cameras WHERE users_id = '{id_user}'")
    if sql.fetchone() is None:
        db.close()
        return "Вы не подписаны ни на одну камеру"
    else:
        ret_value = f"Вы Подписаны на камеры:"
        for value in sql.execute(f"SELECT * FROM cameras INNER JOIN users_cameras ON cameras.id = users_cameras.cameras_id;"):
            ret_value += f"\nНомер: " + value[0]+ "; " + value[1]
        db.close()
        return ret_value
    
# команда get_info
def get_info():
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    ret_value = ""
    for value in sql.execute(f"SELECT * FROM cameras"):
        ret_value += f"\nНомер: " + value[0]+ "; " + value[1]
    db.close()
    return ret_value


# изменение текущего действия пользователя
# это несколько противоречит тз, но при выборе команды она автоматом отправляется, а вписывать ее вручную не так удобно
# и как по мне это самый легкий способ отслеживать действия пользователя
# короче жду критики ¯\_(ツ)_/¯
def change_status_user(id, state):
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    sql.execute(f"UPDATE users SET status = '{state}' WHERE id = '{id}'")
    db.commit()
    db.close()


def get_status_user(id):
    db = sqlite3.connect("mydatabase.db")
    sql = db.cursor()
    for value in sql.execute(f"SELECT status FROM users WHERE id = '{id}'"):
        db.close()
        return value
