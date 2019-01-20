from tkinter import *
from PIL import Image, ImageTk

def resize(pil_img, size):
    w, h = size
    int_size = (int(w), int(h))
    return pil_img.resize(int_size, Image.ANTIALIAS)

root = Tk()
root_size = (600, 600)

root.title('Your pet account')
cv = Canvas(root, width=root_size[0], height=root_size[1], bg='white')      
cv.pack(expand=YES, fill=BOTH)  
root.resizable(False, False)


img_file = "green_blob.png"
org_img = Image.open(img_file)
org_size = org_img.size




def animate_blob():
    w_bound = (500, 400)
    h_bound = (250, 500)

    cycle = 20
    w_speed = (w_bound[1] - w_bound[0]) / cycle
    h_speed = (h_bound[1] - h_bound[0]) / cycle

    cur_size = (w_bound[0], h_bound[0])
    cur_cycle = 0
    while True:
        cur_img = resize(org_img, cur_size)
        tk_img = ImageTk.PhotoImage(cur_img)
        cv_obj = cv.create_image(root_size[0]//2, 520, anchor=S, image=tk_img)
        yield 5 # ms

        cv.delete(cv_obj)
        cur_cycle += 1
        if cur_cycle == cycle:
            cur_cycle = 0
            w_speed = -w_speed
            h_speed = -h_speed
        cur_size = (cur_size[0] + w_speed, cur_size[1] + h_speed)

def animate(iterator):
    root.after(next(iterator), animate, iterator)

animate(animate_blob())
mainloop()