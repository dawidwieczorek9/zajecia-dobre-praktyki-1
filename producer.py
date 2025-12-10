import csv
import os
from filelock import FileLock

FILE = "tasks.csv"
LOCK = "tasks.csv.lock"

def get_next_id():
    if not os.path.exists(FILE):
        return 1
    with open(FILE, "r", newline="") as f:
        rows = list(csv.reader(f))
        if not rows:
            return 1
        return int(rows[-1][0]) + 1

def main():
    new_id = get_next_id()

    with FileLock(LOCK):
        with open(FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([new_id, "pending"])

    print("[Producer] Added task " + str(new_id))

if __name__ == "__main__":
    main()
