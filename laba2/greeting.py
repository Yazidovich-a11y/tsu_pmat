#!/usr/bin/python3

import sys


def is_valid_name(name):
    return name and name[0].isupper() and name.isalpha()


def process_names(input_text):
    for name in input_text.strip().split():
        if is_valid_name(name):
            print(f"Hello, {name}! Nice to see you!")
        else:
            print(f"Error: '{name}' is not a valid name.", file=sys.stderr)


def interactive_mode():
    while True:
        try:
            user_input = input("Enter your name: ").strip()
            if user_input:
                process_names(user_input)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def main():
    if sys.stdin.isatty():
        interactive_mode()
    else:
        for line in sys.stdin:
            process_names(line)


if __name__ == "__main__":
    main()
