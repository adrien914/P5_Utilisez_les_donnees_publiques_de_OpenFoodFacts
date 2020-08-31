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

    def update(self, table: str, data: list, conditions: list):
        data = ",".join(data)
        conditions = ",".join(conditions)
        instruction = "UPDATE " + table + " SET " + data + " WHERE " + conditions
        self.cursor.execute(instruction)
        self.conn.commit()

    def fill_database(self):
        categories = self.open_api.get_categories()
        for category in categories:
            name = "'" + category["name"].replace("'", "\\'") + "'"
            url = "'" + category["url"] + "'"
            print(name)
            if not self.select("category", "name={}".format(name)):
                self.insert("category", ["name", "url"], [name, url])
        categories = self.select("category")
        for category in categories:
            aliments = self.open_api.get_aliments(category)
            for aliment in aliments:
                headers = ["product_name", "category", "nutrition_grades", "stores"]
                aliment["category"] = category[0]
                data = []
                for header in headers:
                    try:
                        data.append("'" + aliment[header].replace("'", "\\'") + "'")
                    except KeyError:
                        data.append("NULL")
                    except AttributeError:
                        data.append(str(aliment[header]))
                self.insert("aliment", headers, data)


