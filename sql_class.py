import pymysql


class connectMySQL:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "Abc123456789@"
        self.port = 3307
        self.database = "neural01"
        self.conn = None
        self.cursor = None
        self.create_table()

    def connect(self):
        """
        Connect to MySQL Database.
        """
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    def get_data(self, sql):
        """
        Common function to get data from the database.
        """
        self.connect()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result

        except Exception as E:
            print(E)
            return

        finally:
            if self.conn:
                self.conn.close()

    def update_data(self, sql):
        """
        Common function to update the database.
        """
        self.connect()

        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as E:
            self.conn.rollback()
            return E
        finally:
            if self.conn:
                self.conn.close()

    def create_login_account(self, user_name, password):
        """
        Insert new login account data.
        """
        sql = f"INSERT INTO user_tb (user_name, password) VALUES ('{user_name}', '{password}')"

        result = self.update_data(sql=sql)

        return result

    def check_username(self, username):
        """
        Check the username when creating a new login account.
        """
        sql = f"SELECT * FROM user_tb WHERE user_name='{username}'"

        result = self.get_data(sql=sql)

        return result

    def create_table(self):
        """
        Create table if it does not exist.
        """
        self.connect()
        try:
            sql = """
            CREATE TABLE IF NOT EXISTS user_tb (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
            """
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as E:
            self.conn.rollback()
            return E
        finally:
            if self.conn:
                self.conn.close()