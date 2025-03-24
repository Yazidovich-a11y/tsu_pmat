#!/usr/bin/python3

import random
import sys


def write_log(content, filename="log1.txt"):
    with open(filename, "a") as log_file:
        log_file.write(content + "\n")


def main():
    number = random.randint(-10, 10)
    log_message = f"Generated number: {number}"
    write_log(log_message)
    print(number, file=sys.stdout)


if __name__ == "__main__":
    main()
