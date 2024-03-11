import os
import psycopg2



class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.environ.get("PG_HOST"),
            database=os.environ.get("PG_DATABASE"),
            user=os.environ.get("PG_USER"),
            password=os.environ.get("PG_PASS"),
            port=os.environ.get("PG_PORT")
        )
        self.cur = self.conn.cursor()

    def query(self, query, params=None):
        self.cur.execute(query, params)
        try:
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return None
    
    def insert(self, query, params=None):
        self.cur.execute(query, params)
        self.commit()

    def update(self, query, params=None):
        self.cur.execute(query, params)
        self.commit()

    def delete(self, query, params=None):
        self.cur.execute(query, params)
        self.commit()

    def rollback(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()