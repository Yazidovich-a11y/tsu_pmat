#!/usr/bin/python3

import sys
import math


def log_message(text, filename="log3.txt"):
    with open(filename, "a") as log_file:
        log_file.write(text + "\n")


def main():
    try:
        num = float(sys.stdin.read().strip())
        log_message(f"Input number: {num}")
        result = math.sqrt(num)
        log_message(f"Square root: {result}")
    except ValueError as e:
        print(str(e), file=sys.stderr)
        log_message(str(e))
    else:
        print(result, file=sys.stdout)


if __name__ == "__main__":
    main()
