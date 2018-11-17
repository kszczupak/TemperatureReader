import sys
import subprocess
import time


def clear_terminal():
    if sys.platform in ["linux", "linux2"]:
        print("\033c")
    elif sys.platform == "win32":
        subprocess.call(["cls"], shell=True)


def print_spinning_cursor(sec):
    def get_cursor_position():
        while True:
            for cursor in '|/-\\':
                yield cursor

    cursor_position = get_cursor_position()
    for _ in range(sec * 10):
        sys.stdout.write(next(cursor_position))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
