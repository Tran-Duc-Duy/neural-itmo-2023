from mysql import connector


class connectMySQL:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = ""
        self.port = 3306
        self.database = "neural01"
        self.my_connector = None
        self.my_cursor = None

    def connect(self):
        """
        Connect to MySQL Database.
        """
        self.my_connector = connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=self.database
        )

        self.my_cursor = self.my_connector.cursor(dictionary=True, buffered=True)

    def get_data(self, sql):
        """
        Common function to get data from database.
        """
        self.connect()
        try:
            self.my_cursor.execute(sql)
            result = self.my_cursor.fetchall()

            return result

        except Exception as E:
            print(E)
            return

        finally:
            if self.my_connector:
                self.my_cursor.close()

    def update_data(self, sql):
        """
        Common function to update database.
        """
        self.connect()

        try:
            self.my_cursor.execute(sql)
            self.my_connector.commit()
        except Exception as E:
            self.my_connector.rollback()
            return E
        finally:
            if self.my_connector:
                self.my_cursor.close()

    ## function for login window
    def create_login_account(self, user_name, password):
        """
        Insert new login account data
        """
        sql = f"INSERT INTO user_tb (user_name, password) VALUES ('{user_name}', '{password}')"

        result = self.update_data(sql=sql)

        return result

    def check_username(self, username):
        """
        Check the username when create new login account.
        """
        sql = f"SELECT * FROM user_tb WHERE user_name='{username}'"

        result = self.get_data(sql=sql)

        return result
