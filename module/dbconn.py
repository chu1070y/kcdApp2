import psycopg2
from configparser import ConfigParser


class Postgres:
    def __init__(self):
        self._conn()

    def _conn(self):
        config = ConfigParser()
        config.read('./config/config.ini')
        config = config['db']

        try:
            self.conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password'])

            self.cursor = self.conn.cursor()

        except Exception as e:
            print("Error while fetching Schema")
            print(e)

    def close(self):
        self.conn.close()







