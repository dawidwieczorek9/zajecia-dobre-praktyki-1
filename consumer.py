import sqlite3
import time

FILE = 'tasks.db'
WORK_DURATION = 30
CHECK_INTERVAL = 5


def do_task(worker_name):
    while True:
        connection = sqlite3.connect(FILE)
        row = connection.execute("SELECT id FROM tasks WHERE status = 'pending' ORDER BY id LIMIT 1").fetchone()
        if row:
            task_id = row[0]
            connection.execute("UPDATE tasks SET status = ?, worker = ?, started_at = ? WHERE id = ? AND status = 'pending'", ('in_progress', worker_name, time.strftime('%Y-%m-%d %H:%M:%S'), task_id))
            connection.commit()
            connection.close()

            print(worker_name + " wykonuje zadanie " + str(task_id) + " przez " + str(WORK_DURATION) + "s")
            time.sleep(WORK_DURATION)

            connection = sqlite3.connect(FILE)
            connection.execute("UPDATE tasks SET status = ?, finished_at = ? WHERE id = ?", ('done', time.strftime('%Y-%m-%d %H:%M:%S'), task_id))
            connection.commit()
            connection.close()
            print(worker_name + " zakończył zadanie " + str(task_id))
        else:
            connection.close()
            time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    worker_name = input("Podaj nazwę konsumenta: ")
    do_task(worker_name)
