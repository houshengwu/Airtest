import pymysql
from datetime import datetime

class MySQLConnector:
    def __init__(self, host, port, user, password, database, charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.conn = None
        self.cursor = None
        

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.password,
                db=self.database,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to MySQL database: {e}")

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, sql):
        try:
            if not self.cursor or not self.conn:
                self.connect()
            
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return rows
        
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        
        finally:
            self.disconnect()

    def execute_insert(self, sql, data):
        try:
            if not self.cursor or not self.conn:
                self.connect()
            
            self.cursor.execute(sql, data)
            self.conn.commit()  # Commit the transaction for inserts
            print("Insert successful")
        
        except Exception as e:
            print(f"Error executing insert: {e}")
        
        finally:
            self.disconnect()

class UpLoadMysql:
    def __init__(self,updata):
        self.data = updata
        self.upload()

    def upload(self):
  # Assuming this is a string representation of time
        now_time = datetime.now()

        mysql_connector = MySQLConnector(
            host='rm-wz9491pt7f24f6a962o.mysql.rds.aliyuncs.com',
            port=3306,
            user='houshengwu',
            password='Hou1286257647',
            database='qq'
        )

        sql_insert = "INSERT INTO `qq_group_chat_content` (`message`, `sender`, `send_time`, `now_time`,`group_name`) VALUES (%s, %s, %s, %s, %s)"
        data = (self.data[1], self.data[3], self.data[0], now_time,self.data[4])

        mysql_connector.execute_insert(sql_insert, data)

if __name__ == "__main__":
    # Create an instance of UpLoadMysql


    upload_mysql = UpLoadMysql(data)
    
    # Call the upload method to insert data into MySQL
    upload_mysql.upload()
