import mysql.connector
from settings import number_of_categories, aliments_per_category
from utils.OpenApi import OpenApi


class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(host="0.0.0.0", port=3306, user="root", password="root", database="myDb")
        self.cursor = self.conn.cursor()
        self.open_api = OpenApi()
        aliments = self.select("aliment")
        if len(aliments) < number_of_categories * aliments_per_category:
            self.fill_database()

    def select(self, table, conditions=None):
        instruction = "SELECT * FROM " + table
        if conditions:
            instruction += " WHERE " + conditions
        print(instruction)

        self.cursor.execute(instruction)
        return self.cursor.fetchall()

    def insert(self, table: str, headers: list, data: list, foreign_id=None):
        headers = ",".join(headers)
        data = ",".join(data)
        if foreign_id:
            data += ", " + str(foreign_id)
        instruction = "INSERT INTO {} ({}) VALUES ({})".format(table, headers, data)
        self.cursor.execute(instruction)
        self.conn.commit()
        return self.cursor.lastrowid

    def fill_database(self):
        categories = self.open_api.get_categories()
        for category in categories:
            name = category["name"].replace("'", "\\'")
            if not self.select("category", "name='{}'".format(name)):
                self.insert("category", ["name"], [category["name"]])

