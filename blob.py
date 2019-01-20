from tkinter import *
from PIL import Image, ImageTk

class Blob:

    W_BOUND = (600, 400)
    W_RANGE = 200
    H_BOUND = (200, 600)
    H_RANGE = 400
    BASE_HALF_CYCLE = 20

    def __init__(self, gui_root, canvas, cv_size, speed=1):
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
        # self.w_bound = (600, 550)
        # self.h_bound = (200, 300)
        self.blob_size = 1
        self.motion_range = 1

        self.base_imgs = {color: Image.open(img_file) for color, img_file in img_files.items()}
        self.cur_base_img = self.base_imgs['g']

        self.tk_img = None

        self.speed = speed

    def set_color(self, color):
        self.cur_base_img = self.base_imgs[color]

    def set_motion_range(self, max_range=1):
        self.motion_range = max_range

    def set_speed(self, speed=1):
        self.speed = speed

    def set_size(self, size=1):
        self.blob_size = size

    def animate(self):
        while True:
            # recalculate all parameters
            half_cycle = int(Blob.BASE_HALF_CYCLE / self.speed)

            print('INFO: half cycle {}'.format(half_cycle))

            self.w_bound = (Blob.W_BOUND[0], Blob.W_BOUND[0] - self.motion_range * Blob.W_RANGE)
            self.h_bound = (Blob.H_BOUND[0], Blob.H_BOUND[0] + self.motion_range * Blob.H_RANGE)
            self.w_bound = tuple(x * self.blob_size for x in self.w_bound)
            self.h_bound = tuple(x * self.blob_size for x in self.h_bound)

            w_speed = (self.w_bound[1] - self.w_bound[0]) / half_cycle
            h_speed = (self.h_bound[1] - self.h_bound[0]) / half_cycle
            cur_size = (self.w_bound[0], self.h_bound[0])

            img_height = self.cv_size[1] * (1 + self.blob_size) / 2

            # perform 1 full cycle of animation
            # 1st half
            for i in range(half_cycle):
                cv_obj = self.show_img(cur_size, img_height)
                yield
                self.cv.delete(cv_obj)
                cur_size = (cur_size[0] + w_speed, cur_size[1] + h_speed)
            # 2nd half
            for i in range(half_cycle):
                cv_obj = self.show_img(cur_size, img_height)
                yield
                self.cv.delete(cv_obj)
                cur_size = (cur_size[0] - w_speed, cur_size[1] - h_speed)

    def show_img(self, size, img_height):
        cur_img = self.resize(self.cur_base_img, size)
        self.tk_img = ImageTk.PhotoImage(cur_img) # prevent garbage collection by using self
        cv_obj = self.cv.create_image(self.cv_size[0]//2, img_height, anchor=S, image=self.tk_img)
        return cv_obj

    def resize(self, pil_img, size):
        w, h = size
        int_size = (int(w), int(h))
        return pil_img.resize(int_size, Image.BILINEAR)
