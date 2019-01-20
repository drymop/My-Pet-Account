from tkinter import *
from PIL import Image, ImageTk
import random
from blob import Blob

def repeat(iterator, sleep_ms=10):
    next(iterator)
    root.after(sleep_ms, repeat, iterator, sleep_ms)

if __name__ == '__main__':

    root = Tk()
    root_size = (600, 600)
    root.title('My pet account')
    cv = Canvas(root, width=root_size[0], height=root_size[1], bg='white')
    cv.pack(expand=YES, fill=BOTH)
    root.resizable(False, False)

    blob = Blob(root, cv, root_size)

    def do_shit():
        color = ['g', 'r', 'y']
        while True:
            c = random.randint(0,2)
            blob.set_color(color[c])
            yield

    repeat(blob.animate(), 1)
    repeat(do_shit(), 100)

    mainloop()

    a = Account()
