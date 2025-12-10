import csv
import time
from filelock import FileLock

FILE = 'tasks.csv'
LOCK = 'tasks.csv.lock'
WORK_DURATION = 30
CHECK_INTERVAL = 5

def do_task(worker_name):
    while True:
        with FileLock(LOCK):
            # wczytujemy wszystkie zadania jako listę list
            tasks = []
            with open(FILE, 'r', newline='') as plik:
                reader = csv.reader(plik)
                for row in reader:
                    # dopisujemy worker i timestamps jeśli brakują (len(row) < 5)
                    while len(row) < 5:
                        row.append('')
                    tasks.append(row)

            task_found = False
            for task in tasks:
                if task[1] == 'pending':  # status jest w drugiej kolumnie
                    task[1] = 'in_progress'
                    task[2] = worker_name
                    task[3] = time.strftime('%Y-%m-%d %H:%M:%S')  # started_at
                    task_found = True
                    task_id = task[0]
                    break

            if task_found:
                with open(FILE, 'w', newline='') as plik:
                    writer = csv.writer(plik)
                    writer.writerows(tasks)

        if task_found:
            print(worker_name + " wykonuje zadanie " + task_id + " przez " + str(WORK_DURATION) + "s")
            time.sleep(WORK_DURATION)

            with FileLock(LOCK):
                with open(FILE, 'r', newline='') as plik:
                    tasks = [row for row in csv.reader(plik)]
                    for row in tasks:
                        while len(row) < 5:
                            row.append('')
                        if row[0] == task_id:
                            row[1] = 'done'
                            row[4] = time.strftime('%Y-%m-%d %H:%M:%S')  # finished_at
                            break
                with open(FILE, 'w', newline='') as plik:
                    writer = csv.writer(plik)
                    writer.writerows(tasks)

            print(worker_name + " zakończył zadanie " + task_id)
        else:
            time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    worker_name = input("Podaj nazwę konsumenta: ")
    do_task(worker_name)
