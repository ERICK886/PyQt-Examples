import sqlite3


class SqlData:
    def __init__(self):
        self.db_name = 'reward.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql_reward = """CREATE TABLE IF NOT EXISTS reward (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            income DECIMAL(10,2) NOT NULL,
            expend DECIMAL(10,2) NOT NULL,
            classify TEXT NOT NULL,
            created_at TEXT NOT NULL
        );"""

        self.cursor.execute(sql_reward)
        self.conn.commit()

    def getReward(self):
        sql_reward = "SELECT * FROM reward"
        self.cursor.execute(sql_reward)
        results = self.cursor.fetchall()
        return results

    def addReward(self, income, expend, classify, created_at):
        try:
            sql_reward = "INSERT INTO reward (income, expend, classify, created_at) VALUES (?,?,?,?)"
            self.cursor.execute(sql_reward, (income, expend, classify, created_at))
            self.conn.commit()
            return True
        except Exception as e:
            return str(e)

    def updateReward(self, id, income, expend, classify, created_at):
        sql_reward = "UPDATE reward SET income=?, expend=?, classify=?, created_at=? WHERE id=?"
        self.cursor.execute(sql_reward, (income, expend, classify, created_at, id))
        self.conn.commit()

    def deleteReward(self, id):
        try:
            sql_reward = "DELETE FROM reward WHERE id=?"
            self.cursor.execute(sql_reward, (id,))
            self.conn.commit()
            return True
        except Exception as e:
            return str(e)