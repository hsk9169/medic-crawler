from info import DB_INFO
import pymysql

class DbClient:
    def __init__(self):
        self.db = ''
        self.cursor = ''
        self.host =     DB_INFO['host'] 
        self.port =     DB_INFO['port'] 
        self.user =     DB_INFO['user'] 
        self.password = DB_INFO['password']
        self.database = DB_INFO['database']

    def connectDb(self):
        try:
            connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password
            )
            self.db = connection
            self.cursor = connection.cursor()
            version = self.cursor.execute("select version()")
            assert version == 1
        except Exception as err:
            print(err)
    
    def dropDb(self):
        try:
            res = self.cursor.execute(f'drop database {self.database}')
            assert res == 0
        except Exception as err:
            print(err)

    def createDb(self):
        try:
            res = self.cursor.execute(f'create database {self.database}')
            assert res == 1 
            self.cursor.connection.commit()
            self.cursor.execute(f'use {self.database}')
        except Exception as err:
            print(err)
    
    def createTable(self):
        try:
            sql = '''
                create table hospital (
                    id int not null auto_increment,
                    name text,
                    address text,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    primary key (id)
                )
                '''
            res = self.cursor.execute(sql)
            assert res == 0
        except Exception as err:
            print(err)

    def addRow(self, name, address):
        sql = '''
            insert into hospital(name, address) values ('%s', '%s')
            ''' % (name, address)
        try:
            self.cursor.execute(sql)
            print('db insert query executed')
        except Exception as err:
            print('db query execution failed')
            print(err)

    def commitQueries(self):
        try:
            self.db.commit()
            print('db commit executed')
        except Exception as err:
            print('db commit execution failed')
            print(err)

    def fetchAll(self):
        sql = '''select * from hospital'''
        try:
            res = self.cursor.execute(sql)
            res = self.cursor.fetchall()
            print(res)
        except Exception as err:
            print(err)

    def getRowNum(self):
        sql = '''select * from hospital'''
        try:
            res = self.cursor.execute(sql)
            return res
        except Exception as err:
            print(err)
            return False

    def close(self):
        try:
            self.db.close()
        except Exception as err:
            print(err)
