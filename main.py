from tkinter import *
from PIL import Image, ImageTk

from blob import Blob


def repeat(iterator, sleep_ms=10):
    next(iterator)
    root.after(sleep_ms, repeat, iterator, sleep_ms)

root = Tk()
root_size = (600, 600)
root.title('My pet account')
cv = Canvas(root, width=root_size[0], height=root_size[1], bg='white')      
cv.pack(expand=YES, fill=BOTH)  
root.resizable(False, False)

blob = Blob(root, cv, root_size)

def do_shit():
    color = ['g', 'r', 'y']
    speed = [1, 0.3]
    motion = [1, 0.3]
    while True:
        for m, s in zip(motion, speed):
            blob.set_motion_range(m)
            blob.set_speed(s)
            yield
            
repeat(blob.animate(), 10)
repeat(do_shit(), 3000)

mainloop()