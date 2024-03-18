import sqlite3

class UserModel:
    def __init__(self,
                 chat_id,
                 session_file=None,
                 is_auth=None,
                 phone_number=None,
                 password=None) -> None:

        self.chat_id = chat_id
        self.session_file = session_file
        self.is_auth = is_auth
        self.phone_number = phone_number
        self.password = password


class UserController:
    def __init__(self, connection, cursor) -> None:
        self.connection:sqlite3.Connection = connection
        self.cursor:sqlite3.Cursor = cursor


    def get_user(self, sql, parameters):
        self.cursor.execute(sql, parameters)
        user_data = self.cursor.fetchone()

        if user_data:
            return user_data

    def get_user_status(self, chat_id):
        self.cursor.execute("SELECT chat_id FROM users WHERE chat_id = ?", (chat_id,))
        status = self.cursor.fetchone()

        if status:
            return status
        else:
            return None

    def update_user(self, sql, parameters):
        self.cursor.execute(sql, parameters)
        self.connection.commit()

    def delete_user(self, chat_id):
        self.cursor.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
        self.conn.commit()

    def add_user(self, user):
        self.cursor.execute('''INSERT INTO users (chat_id) VALUES (?)''', (user.chat_id,))
        self.connection.commit()
