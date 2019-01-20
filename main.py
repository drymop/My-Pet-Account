from tkinter import *
from PIL import Image, ImageTk
import random
from blob import Blob
import math
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

    def do_shit(a, blob):
        while True:
            m, b, bal = a.update()
            if m == 0:
                m += 1e-3
            print('m: {}; b: {}; bal: {}'.format(m,b,bal))
            blob.set_size(math.log(bal)/10)
            # blob.set_speed(m)
            if m > 5:
                blob.set_color('g')
                blob.set_motion_range(1)
                blob.set_speed(1)
            elif m < -5:
                blob.set_color('r')
                blob.set_motion_range(0.2)
                blob.set_speed(0.2)
            else:
                blob.set_color('y')
                blob.set_motion_range(0.8)
                blob.set_speed(0.8)
            yield

    DEFAULT_ACCOUNT_ID = '5c43b4ca322fa06b677943fc'
    repeat(blob.animate(), 10)

    acc = Account(DEFAULT_ACCOUNT_ID)


    repeat(do_shit(acc, blob), 10000)
    mainloop()
