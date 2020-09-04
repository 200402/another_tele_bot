import sqlite3

# создание таблиц
def create_table():
    with sqlite3.connect("mydatabase.db") as db:
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

# добавление юзеров
def add_users():
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        users_id = ['454054254', "123212", "12312212"]
        for user_id in users_id:
            sql.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO users VALUES (?,?)", (user_id,"calmness",))


# добавление камер
def add_cameras():
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        cameras_id = ['1', "3", "4"]
        for camera_id in cameras_id:
            sql.execute(f"SELECT id FROM cameras WHERE id = '{camera_id}'")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO cameras VALUES (?,?)", (camera_id,"инфа о камере",))
        

# есть ли у юзера доступ к боту
def does_the_user_have_access(id):
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        sql.execute(f"SELECT id FROM users WHERE id = '{id}'")
        if sql.fetchone() is None: 
            return False
        else:
            return True

# команда sub
def sub(id_user, id_camera):
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        sql.execute(f"SELECT * FROM cameras WHERE id = '{id_camera}'")
        if sql.fetchone() is None: 
            return "Нет камеры с таким номером"
        else:
            sql.execute(f"SELECT * FROM users_cameras WHERE users_id = '{id_user}' AND cameras_id = '{id_camera}'")
            if sql.fetchone() is None:
                sql.execute(f"INSERT INTO users_cameras VALUES (?,?)", (id_user, id_camera,))
                return f"Вы успешно подписались на камеру с номером {id_camera}"
            else:
                return f"Вы уже подписаны на камеру с номером {id_camera}"


# команда stop
def stop(id_user, id_camera):
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        sql.execute(f"SELECT * FROM cameras WHERE id = '{id_camera}'")
        if id_camera.lower() == "all":
            sql.execute(f"DELETE FROM users_cameras WHERE users_id = '{id_user}'")
            return "Вы отменили все свои подписки"
        elif sql.fetchone() is None:
            return "Нет камеры с таким номером"
        else:
            sql.execute(f"SELECT * FROM users_cameras WHERE users_id = '{id_user}' AND cameras_id = '{id_camera}'")
            if sql.fetchone() is None:
                return f"Вы не были подписаны на камеру с номером {id_camera}"
            else:
                sql.execute(f"DELETE FROM users_cameras WHERE users_id = '{id_user}' AND cameras_id = '{id_camera}'")
                return f"Вы отменили подписку на камеру с номером {id_camera}"


# команда cameras
def cameras(id_user):
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        sql.execute(f"SELECT * FROM users_cameras WHERE users_id = '{id_user}'")
        if sql.fetchone() is None: 
            return "Вы не подписаны ни на одну камеру"
        else:
            ret_value = f"Вы Подписаны на камеры:"
            for value in sql.execute(f"SELECT * FROM cameras INNER JOIN users_cameras ON cameras.id = users_cameras.cameras_id;"):
                ret_value += f"\nНомер: " + value[0]+ "; " + value[1] 
            return ret_value
    
# команда get_info
def get_info():
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        ret_value = ""
        for value in sql.execute(f"SELECT * FROM cameras"):
            ret_value += f"\nНомер: " + value[0]+ "; " + value[1] 
        return ret_value


# изменение текущего действия пользователя
# это несколько противоречит тз, но при выборе команды она автоматом отправляется, а вписывать ее вручную не так удобно
# и как по мне это самый легкий способ отслеживать действия пользователя
# короче жду критики ¯\_(ツ)_/¯
def change_status_user(user_id, state):
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        sql.execute(f"UPDATE users SET status = '{state}' WHERE id = '{user_id}'") 


def get_status_user(id):
    with sqlite3.connect("mydatabase.db") as db:
        sql = db.cursor()
        for value in sql.execute(f"SELECT status FROM users WHERE id = '{id}'"):
            return value
