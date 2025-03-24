#!/usr/bin/python3

import random
import sys


def log_message(text, filename="log2.txt"):
    with open(filename, "a") as log_file:
        log_file.write(text + "\n")


def main():
    try:
        num = int(sys.stdin.read().strip())
        random_num = random.randint(-10, 10)
        log_message(f"Input number: {num}, Random number: {random_num}")
        result = num / random_num
        log_message(f"Result: {result}")
    except ZeroDivisionError:
        error_msg = "Error: Division by zero!"
        print(error_msg, file=sys.stderr)
        log_message(error_msg)
    except ValueError:
        error_msg = "Error: Invalid input! Expected an integer."
        print(error_msg, file=sys.stderr)
        log_message(error_msg)
    else:
        print(result, file=sys.stdout)


if __name__ == "__main__":
    main()
