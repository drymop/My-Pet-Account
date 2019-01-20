from tkinter import *
from PIL import Image, ImageTk
import random
from blob import Blob
from account import Account

def repeat(iterator, sleep_ms=10, idle=False):
    next(iterator)
    if idle:
        root.after_idle(repeat, iterator)
    else:
        root.after(sleep_ms, repeat, iterator, sleep_ms)

if __name__ == '__main__':

    root = Tk()
    root_size = (600, 600)
    root.title('My pet account')
    cv = Canvas(root, width=root_size[0], height=root_size[1], bg='white')
    cv.pack(expand=YES, fill=BOTH)
    root.resizable(False, False)

    blob = Blob(root, cv, root_size)

    def do_shit(a):
        while True:
            a.update()
            yield

    DEFAULT_ACCOUNT_ID = '5c43b4ca322fa06b677943fc'
    repeat(blob.animate(), 10)

    acc = Account(DEFAULT_ACCOUNT_ID)


    repeat(do_shit(acc), 0, idle=True)
    mainloop()
