import os
import sys
from time import sleep
from pynput.keyboard import Key, Controller

keyboard = Controller()


def press_key(key):
    keyboard.press(key)
    keyboard.release(key)


def type_word(word):
    keyboard.type(word)
    press_key(Key.enter)


def send_words(source, timeout):
    for word in source:
        type_word(word)
        sleep(timeout)


if __name__ == '__main__':
    if len(sys.argv) < 2 or not os.path.isfile(sys.argv[1]):
        print('Clicker usage: python3 clicker.py <source> [arguments]\nARGUMENTS:\n  --split-by-lines - send not alone '
              'words, but whole lines\n  --begin-timeout <seconds> - wait n seconds before beginning\n  --timeout - wai'
              't n seconds between sending\n  --infinity-duration - send file content again and again')
        sys.exit()

    file = sys.argv[1]

    with open(file, 'r') as source:
        # at first, split by lines
        source = source.read().splitlines()

    if '--split-by-lines' not in sys.argv:
        # then, split each line by spaces
        temp = []

        for line in source:
            temp += line.split()

        source = temp

    if '--begin-timeout' in sys.argv:
        sleep(float(sys.argv[sys.argv.index('--begin-timeout') + 1]))

    timeout = 0 if '--timeout' not in sys.argv else float(sys.argv[sys.argv.index('--timeout') + 1])

    # mainloop
    try:
        if '--infinity-duration' not in sys.argv:
            send_words(source, timeout)
        else:
            while True:
                send_words(source, timeout)
                sleep(1)
    except KeyboardInterrupt:
        print('\nQuitting...')

