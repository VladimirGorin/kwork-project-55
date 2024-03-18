import sqlite3

class AdsModel:
    def __init__(self,
                 owner_id,
                 link,
                 status=None) -> None:

        self.owner_id = owner_id
        self.link = link
        self.status = status

class AdsController:
    def __init__(self, connection, cursor) -> None:
        self.connection:sqlite3.Connection = connection
        self.cursor:sqlite3.Cursor = cursor


    def get_ads(self, sql, parameters, fetchmethod="one"):
        self.cursor.execute(sql, parameters)

        if fetchmethod == "one":
            ads_data = self.cursor.fetchone()
        elif fetchmethod == "all":
            ads_data = self.cursor.fetchall()


        if ads_data:
            return ads_data

    def get_ads_status(self, owner_id):
        self.cursor.execute("SELECT owner_id FROM ads WHERE owner_id = ?", (owner_id,))
        status = self.cursor.fetchone()

        if status:
            return status
        else:
            return None

    def update_ads(self, sql, parameters):
        self.cursor.execute(sql, parameters)
        self.connection.commit()

    def delete_ads(self, owner_id):
        self.cursor.execute("DELETE FROM ads WHERE owner_id=?", (owner_id,))
        self.conn.commit()

    def add_ads(self, ads:AdsModel):
        self.cursor.execute('''INSERT INTO ads (owner_id, link) VALUES (?, ?)''', (ads.owner_id, ads.link))
        self.connection.commit()
