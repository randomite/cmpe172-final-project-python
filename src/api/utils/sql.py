from flaskext.mysql import MySQL


class sql:

    dbc = ("localhost","root","root","employees")

    mysql = MySQL()

    def __init__(self):
        conn = self.mysql.connect()
        self.cursor = conn.cursor()

    def query(self,sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def rows(self):
        return self.cursor.rowcount
