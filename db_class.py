import psycopg2
import json
import os

db_uri = os.environ['DATABASE_URL']


class methods():
    """PostgreSQL Database class."""
    def __init__(self, uri):
        self.URI = uri
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        print('database connecting')
        if self.conn is None:
            self.conn = psycopg2.connect(self.URI)
            print('database connected')

    def login(self, username, password):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user_info WHERE name ='"+username+"' AND pw ='"+password+"';")
        res = cur.fetchone()
        cur.close()
        if res is not None:
            _,name,_,location,age = res
            return {'name':name,'location':location,'age':age}
        return False

    #availablility for username
    def taken(self,username): 
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user_info WHERE name ='"+username+"';")
        res = cur.fetchone()
        cur.close()
        if res is not None:
            print('username is taken')
            return True
        print('username is not taken')
        return False

    def signup(self, username,password,age,location):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user_info(name,pw,age,location) VALUES('"+username+"','"+password+"',"+age+",'"+location+"');")
        self.conn.commit()
        cur.close()
        print(username+' has succesfully signed up!')