import psycopg2
import json
'''
load in config object
with open('auth.json') as r:
    config = json.load(r)
'''
config = {
    "host":"postgres://scviszuljxwilm:2c5d439483ffb7ad22a83d6ea32525c451f20c148f39ef8049dc322ca683e458@ec2-54-172-173-58.compute-1.amazonaws.com:5432/dd0v3nsutfj8g4",
    "username":"postgres",
    "password":"leezheng",
    "port":"5432",
    "database":"summer_connecter"
}
class methods():
    """PostgreSQL Database class."""
    def __init__(self, config):
        self.host = config['host']
        self.username = config['username']
        self.pw = config['password']
        self.port = config['port']
        self.dbname = config['database']
        self.conn = None

    def connect(self):
        """Connect to a Postgres database."""
        if self.conn is None:
            self.conn = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.pw,
                port=self.port,
                database=self.dbname
            )
            print('database connected')

    def login(self, username, password):
        self.connect()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM user_info "
                        f"WHERE name ='{username}' "
                        f"AND pw ='{password}';")
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
        cur.execute("SELECT * FROM user_info "
                    f"WHERE name ='{username}';")
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
        cur.execute("INSERT INTO user_info(name,pw,age,location) "
                        f"VALUES('{username}','{password}',{age},'{location}');")
        self.conn.commit()
        cur.close()
        print(username+' has succesfully signed up!')
 



    
