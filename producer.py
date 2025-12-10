import sqlite3

FILE = 'tasks.db'


def create_table():
    connection = sqlite3.connect(FILE)
    connection.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, status TEXT, worker TEXT, started_at TEXT, finished_at TEXT)')
    connection.commit()
    connection.close()


def add_task():
    connection = sqlite3.connect(FILE)
    connection.execute('INSERT INTO tasks (status, worker, started_at, finished_at) VALUES (?, ?, ?, ?)', ('pending', '', '', ''))
    task_id = connection.execute('SELECT last_insert_rowid()').fetchone()[0]
    connection.commit()
    connection.close()
    print("[Producer] Added task " + str(task_id))


if __name__ == '__main__':
    create_table()
    add_task()
