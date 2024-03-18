import sqlite3

class InfoModel:
    def __init__(self,
                 owner_id,
                 place=None,
                 max_price=None,
                 max_days=None,
                 from_time=None,
                 to_time=None) -> None:

        self.owner_id = owner_id
        self.place = place
        self.max_price = max_price
        self.max_days = max_days
        self.from_time = from_time
        self.to_time = to_time

class InfoController:
    def __init__(self, connection, cursor) -> None:
        self.connection:sqlite3.Connection = connection
        self.cursor:sqlite3.Cursor = cursor


    def get_user_info(self, sql, parameters):
        self.cursor.execute(sql, parameters)
        user_info_data = self.cursor.fetchone()

        if user_info_data:
            return user_info_data

    def get_user_info_status(self, owner_id):
        self.cursor.execute("SELECT owner_id FROM users_info WHERE owner_id = ?", (owner_id,))
        status = self.cursor.fetchone()

        if status:
            return status
        else:
            return None

    def update_user_info(self, sql, parameters):
        self.cursor.execute(sql, parameters)
        self.connection.commit()

    def delete_user_info(self, owner_id):
        self.cursor.execute("DELETE FROM users_info WHERE owner_id=?", (owner_id,))
        self.conn.commit()

    def add_user_info(self, user_info:InfoModel):
        self.cursor.execute('''INSERT INTO users_info (owner_id) VALUES (?)''', (user_info.owner_id,))
        self.connection.commit()
