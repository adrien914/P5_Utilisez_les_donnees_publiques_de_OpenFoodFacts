import mysql.connector


class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(host="0.0.0.0", port=3306, user="user", password="test", database="myDb")
        self.cursor = self.conn.cursor()

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
        print(instruction)
        self.cursor.execute(instruction)
        self.conn.commit()
        return self.cursor.lastrowid
