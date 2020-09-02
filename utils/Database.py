import mysql.connector
from settings import number_of_categories, aliments_per_category
from utils.OpenApi import OpenApi


class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(host="0.0.0.0", port=3306, user="root", password="root", database="myDb")
        self.cursor = self.conn.cursor()
        aliments = self.select("aliment")
        if len(aliments) < number_of_categories * aliments_per_category:
            print("initialisation de la base de données...")
            self.fill_database()

    def select(self, table, conditions=None) -> list:
        """
        Generates and executes a select request to the database
        :param table: which table to execute the request on
        :param conditions: the where conditions for the request ( None by default )
        :return: the list returned by the select request
        """
        instruction = "SELECT * FROM " + table
        if conditions:
            instruction += " WHERE " + conditions
        self.cursor.execute(instruction)
        return self.cursor.fetchall()

    def insert(self, table: str, headers: list, data: list, foreign_id=None) -> int:
        """
        Generates and executes an insert request to the database
        :param table: which table to execute the request on
        :param headers: the headers for the insert request
        :param data: the data for the insert request
        :param foreign_id: the foreign id if needed ( optional )
        :return: the id of the inserted row
        """
        headers = ",".join(headers)
        data = ",".join(data)
        if foreign_id:
            data += ", " + str(foreign_id)
        instruction = "INSERT INTO {} ({}) VALUES ({})".format(table, headers, data)
        self.cursor.execute(instruction)
        self.conn.commit()
        return self.cursor.lastrowid

    def update(self, table: str, data: list, conditions: list) -> None:
        """
        Updates a database table
        :param table: which table to execute the request on
        :param data: the data for the update
        :param conditions: the conditions for the update
        :return: None
        """
        data = ",".join(data)
        conditions = ",".join(conditions)
        instruction = "UPDATE " + table + " SET " + data + " WHERE " + conditions
        self.cursor.execute(instruction)
        self.conn.commit()

    def fill_database(self) -> None:
        """
        This function initiates the database with all the data needed
        :return: None
        """
        categories = OpenApi().get_categories()
        for category in categories:
            name = "'" + category["name"].replace("'", "\\'") + "'"
            url = "'" + category["url"] + "'"
            if not self.select("category", "name={}".format(name)):
                self.insert("category", ["name", "url"], [name, url])
        categories = self.select("category")
        for category in categories:
            aliments = OpenApi().get_aliments(category)
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


