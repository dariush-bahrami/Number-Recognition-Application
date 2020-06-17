"""Number Recognition Application for testing deep learning models
"""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import io
from PIL import Image
from number_recognition_tools import predict_number_image

MODELS_FOLDER = Path('trained_models')
MODELS_PATH = [model for model in MODELS_FOLDER.iterdir()]


def extract_model_name(model_name):
    """Extract model name from it's path"""
    return (str(model_name).split('\\')[1]).split('.')[0]


MODELS_NAME = [extract_model_name(model) for model in MODELS_PATH]
MODELS_DICT = {k: v for (k, v) in zip(MODELS_NAME, MODELS_PATH)}

IMAGE_FOLDER = Path('number_images')
IMAGE_NAME = Path('drawed_image.png')
IMAGE_PATH = Path.joinpath(IMAGE_FOLDER, IMAGE_NAME)


class NumberRecognitionInterface:
    """ A class for GUI Packaging"""

    def __init__(self):
        main_window = tk.Tk(className='dAriush Number Recognition AI')
        window_size = (1100, 500)
        main_window.geometry(f"{window_size[0]}x{window_size[1]}")
        main_window.configure(bg='#006266')
        button_font = ("Karla", 12, "bold")
        menu_font = ("Karla", 10, 'bold')
        result_label_font = ("Karla", 15, "bold")
        canvas_background_color = 'white'
        canvas_size = (500, 500)
        self.drawing_area = tk.Canvas(main_window,
                                      bg=canvas_background_color,
                                      height=canvas_size[1],
                                      width=canvas_size[0])

        self.is_mouse_clicked = False
        self.drawing_area.bind("<Motion>", self.draw)
        self.drawing_area.bind("<ButtonPress-1>", self.mouse_clicked_in_canvas)
        self.drawing_area.bind("<ButtonRelease-1>",
                               self.mouse_released_in_canvas)
        self.drawing_area.grid(row=0, column=0, rowspan=3)

        clear_button = tk.Button(main_window, text='Clear All',
                                 command=self.clear_canvas,
                                 height=1,
                                 width=50)
        clear_button.configure(font=button_font, bg='#cd84f1', bd=3,
                               activebackground='#c56cf0')
        clear_button.grid(row=2, column=1, columnspan=2)

        combobox_label = tk.Label(main_window, text='Choose Model: ')
        combobox_label.configure(font=menu_font, bg='#ffcccc')
        combobox_label.grid(row=0, column=1, sticky=tk.E)

        self.models_combobox = ttk.Combobox(main_window, width=47, height=5,
                                            values=MODELS_NAME)
        self.models_combobox.current(0)
        self.models_combobox.configure(font=menu_font)
        self.models_combobox.grid(row=0, column=2)

        self.guess_label = tk.Label(main_window, text="draw a number!",
                                    height=1,
                                    width=20)
        self.guess_label.configure(font=result_label_font, bg='#fc5c65')
        self.guess_label.grid(row=1, column=2)

        guess_button = tk.Button(main_window, text='Guess!!',
                                 command=self.guess_image,
                                 height=1,
                                 width=10)
        guess_button.configure(font=button_font, bg='#2ecc71', bd=3,
                               activebackground='#1abc9c')
        guess_button.grid(row=1, column=1, padx=10)

        main_window.mainloop()

    def draw(self, event):
        """ canvas updating method"""
        if self.is_mouse_clicked:
            self.x_end = event.x
            self.y_end = event.y
            event.widget.create_line(self.x_start, self.y_start,
                                     self.x_end, self.y_end,
                                     smooth=tk.TRUE, fill="black", width=10)

            self.x_start = event.x
            self.y_start = event.y

    def mouse_clicked_in_canvas(self, event):
        """mouse click method"""
        self.is_mouse_clicked = True
        self.x_start = event.x
        self.y_start = event.y

    def mouse_released_in_canvas(self, event):
        """mouse release method"""
        self.is_mouse_clicked = False

    def clear_canvas(self):
        """clear canvas method"""
        self.drawing_area.delete("all")

    def save_as_png(self):
        """saving method"""
        print('Saving!')
        post_script = self.drawing_area.postscript(colormode='color')
        img = Image.open(io.BytesIO(post_script.encode('utf-8')))
        img.save(IMAGE_PATH, 'png')
        print('Saved!')

    def guess_image(self):
        """AI gues method"""
        self.save_as_png()
        current_model_path = MODELS_DICT[self.models_combobox.get()]
        model_guess = predict_number_image(current_model_path, IMAGE_PATH)
        self.guess_label['text'] = model_guess


if __name__ == '__main__':
    NumberRecognitionInterface()
