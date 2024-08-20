# backend.py
import sqlite3 as sql


class TransactionObject:
    database = "clientes.db"
    conn = None
    cur = None
    connected = False

    def connect(self):
        TransactionObject.conn = sql.connect(TransactionObject.database)
        TransactionObject.cur = TransactionObject.conn.cursor()
        TransactionObject.connected = True

    def disconnect(self):
        if TransactionObject.connected:
            TransactionObject.conn.close()
            TransactionObject.connected = False

    def execute(self, sql_query, parms=None):
        if TransactionObject.connected:
            if parms is None:
                TransactionObject.cur.execute(sql_query)
            else:
                TransactionObject.cur.execute(sql_query, parms)
            return True
        else:
            return False

    def fetchall(self):
        if TransactionObject.connected:
            return TransactionObject.cur.fetchall()
        else:
            return None

    def persist(self):
        if TransactionObject.connected:
            TransactionObject.conn.commit()
            return True
        else:
            return False

    def initDB(self):
        self.connect()
        self.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY, 
                nome TEXT, 
                sobrenome TEXT, 
                email TEXT, 
                cpf TEXT
            )
        """)
        self.persist()
        self.disconnect()


# Inicializa o banco de dados criando a tabela se ela não existir
if __name__ == "__main__":
    TransactionObject().initDB()
