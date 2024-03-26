import os
import psycopg2

class Database:
    def __init__(self):
        pass

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=os.environ.get("PG_HOST"),
                database=os.environ.get("PG_DATABASE"),
                user=os.environ.get("PG_USER"),
                password=os.environ.get("PG_PASS"),
                port=os.environ.get("PG_PORT")
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(e)

    def close(self):
        self.cur.close()
        self.conn.close()

    def create(self, query):
        self.connect()
        self.cur.execute(query)
        self.commit()
        self.close()

    def query(self, query, params=None):
        self.connect()
        self.cur.execute(query, params)
        try:
            data = self.cur.fetchall()
            self.close()
            return data
        except Exception as e:
            print(e)
            self.close()
            return None
    
    def insert(self, query, params=None):
        self.connect()
        self.cur.execute(query, params)
        self.commit()
        self.close()

    def update(self, query, params=None):
        self.connect()
        self.cur.execute(query, params)
        self.commit()
        self.close()

    def delete(self, query, params=None):
        self.connect()
        self.cur.execute(query, params)
        self.commit()
        self.close()

    def rollback(self):
        self.connect()
        self.conn.rollback()
        self.close()

    def commit(self):
        self.connect()  
        self.conn.commit()
        self.close()
