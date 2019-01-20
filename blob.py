from tkinter import *
from PIL import Image, ImageTk

class Blob:

    W_BOUND = (600, 400)
    H_BOUND = (200, 600)
    N_KEY_FRAMES = 50
    BASE_SIZE = 100
    
    def __init__(self, gui_root, canvas, cv_size):
        self.gui_root = gui_root
        self.cv = canvas
        self.cv_size = cv_size

        # load image
        img_files = {
            'g': "green_blob.png",
            'y': "yellow_blob.png",
            'r': "red_blob.png",
        }

        # size of blob
        self.w_bound = (600, 400)
        self.h_bound = (200, 600)

        self.base_imgs = {color: Image.open(img_file) for color, img_file in img_files.items()}
        self.cur_base_img = self.base_imgs['g']

        self.tk_img = None

    def set_color(self, color):
        self.cur_base_img = self.base_imgs[color]

    def animate(self):
        w_bound = (600, 400)
        h_bound = (200, 600)

        half_cycle = 15
        w_speed = (self.w_bound[1] - self.w_bound[0]) / half_cycle
        h_speed = (self.h_bound[1] - self.h_bound[0]) / half_cycle

        cur_size = (w_bound[0], h_bound[0])
        cur_cycle = 0
        while True:

            cv_obj = self.show_img(cur_size)
            yield

            self.cv.delete(cv_obj)
            cur_cycle += 1
            if cur_cycle == half_cycle:
                cur_cycle = 0
                w_speed = -w_speed
                h_speed = -h_speed
            cur_size = (cur_size[0] + w_speed, cur_size[1] + h_speed)

    def show_img(self, size):
        cur_img = self.resize(self.cur_base_img, size)
        self.tk_img = ImageTk.PhotoImage(cur_img) # prevent garbage collection by using self
        cv_obj = self.cv.create_image(self.cv_size[0]//2, self.cv_size[1], anchor=S, image=self.tk_img)
        return cv_obj

    def resize(self, pil_img, size):
        w, h = size
        int_size = (int(w), int(h))
        return pil_img.resize(int_size, Image.BILINEAR)