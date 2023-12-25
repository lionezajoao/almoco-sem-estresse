import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

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
        return self.cur.fetchall()
    
    def insert(self, query, params=None):
        self.cur.execute(query, params)
        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()