import tkinter

import customtkinter
from customtkinter import filedialog
from PIL import Image

from io_handler import validate_image
from filter_generator import create_edge_detector
from filter_generator import create_standard_blur
from filter_generator import create_gaussian_blur

APP_FONT = "Roboto"
TITLE_SIZE = 24
SUBHEADING_SIZE = 16
POPUP_SIZE = 14
CENTER_COLUMN = 1
BUTTON_PADX, BUTTON_PADY = 5, 5
radio_button_row = 0
selected_filter = 0

class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create title
        self.title_label = customtkinter.CTkLabel(self, text="Image Filterer", font=(APP_FONT, TITLE_SIZE))
        self.title_label.grid(column=0, sticky="n", columnspan=3)

        # Create explanation and example
        self.explanation = customtkinter.CTkLabel(self, text="Upload an image and choose a filter to modify the image.",
                                             font=(APP_FONT, SUBHEADING_SIZE))
        self.explanation.grid(column=0, columnspan=3, sticky="ew")

        self.example = customtkinter.CTkLabel(self, text="Example", font=(APP_FONT, SUBHEADING_SIZE))
        self.example.grid(column=CENTER_COLUMN)
        self.example_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg")
        self.example_width, example_height = self.example_image.size
        self.example_image_ctk = customtkinter.CTkImage(light_image=self.example_image, dark_image=self.example_image,
                                                   size=(self.example_width, example_height))
        self.example_image_label = customtkinter.CTkLabel(self, image=self.example_image_ctk, text="")
        #self.example_image_label.grid(column=CENTER_COLUMN)

        # Create upload image button
        self.upload_image_label = customtkinter.CTkLabel(self, text="Upload an image (.png & .jpeg accepted)", font=(APP_FONT, SUBHEADING_SIZE - 2))
        self.upload_image_label.grid(column=CENTER_COLUMN)
        self.upload_image_button = customtkinter.CTkButton(self, text="Upload image", command=lambda: upload_new_image(self))
        self.upload_image_button.grid(column=CENTER_COLUMN, pady=5)
        self.UPLOAD_BUTTON_ROW = self.upload_image_button.grid_info()['row']

        # Saved images database
        # TODO: implement; have it so that it dynamically changes rows
       # saved_images_label = customtkinter.CTkLabel(self, text="Saved Images", font=(APP_FONT, SUBHEADING_SIZE))
       # saved_images_label.grid(column=CENTER_COLUMN)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_columnconfigure((0,1,2), weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1)
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        self.geometry(f"{window_width}x{window_height}-10+0")
        self.my_frame = MyFrame(master=self, width=window_width, height=window_height, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")


# Upload image button
def upload_new_image(self):
    filepath = filedialog.askopenfile().name
    if validate_image(filepath):
        display_uploaded_image(self, filepath)
    else: # TODO: do this better
        error_popup = customtkinter.CTkFrame(self, width=300, height=150, corner_radius=10)
        error_popup.place(relx=0.5, rely=0.5, anchor="center")

        error_message = customtkinter.CTkLabel(error_popup, text="File type not supported", font=(APP_FONT, POPUP_SIZE))
        error_message.pack()
        ok_button = customtkinter.CTkButton(error_popup, text="Ok", command=error_popup.destroy)
        ok_button.pack()
        return ""

def display_uploaded_image(self, filepath):
    # Display uploaded image
    image_filename = filepath
    uploaded_image = Image.open(image_filename)
    # TODO: show a scaled down version of the image
    window_width, window_height = uploaded_image.size
    uploaded_image_ctk = customtkinter.CTkImage(light_image=uploaded_image, dark_image=uploaded_image,
                                                    size=(window_width, window_height))
    image_label = customtkinter.CTkLabel(self, image=uploaded_image_ctk, text="")
    image_label.grid(column=CENTER_COLUMN)
    display_radio_buttons(self, uploaded_image)

def display_radio_buttons(self, image):
    selected_filter = tkinter.IntVar(value=0)
    edge_detector_num = 1
    standard_blur_num = 2
    gaussian_blur_num = 3
    edge_detector_button = customtkinter.CTkRadioButton(self, text="Edge Detector",
                                                        command=lambda:filter_button_event(self, image, edge_detector_num),
                                                        variable=selected_filter, value=edge_detector_num)
    standard_blur_button = customtkinter.CTkRadioButton(self, text="Standard Blur",
                                                        command=lambda:filter_button_event(self, image, standard_blur_num),
                                                        variable=selected_filter, value=standard_blur_num)
    gaussian_blur_button = customtkinter.CTkRadioButton(self, text="Gaussian Blur",
                                                        command=lambda:filter_button_event(self, image, gaussian_blur_num),
                                                        variable=selected_filter, value=gaussian_blur_num)

    edge_detector_button.grid(column=0, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="e")
    radio_button_row = edge_detector_button.grid_info()['row']
    standard_blur_button.grid(column=1, row=radio_button_row, padx=BUTTON_PADX, pady=BUTTON_PADY)
    gaussian_blur_button.grid(column=2, row=radio_button_row, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")


def display_filtered_image(self, image):
    filtered_image_width, filtered_image_height = image.size
    filtered_image_ctk = customtkinter.CTkImage(light_image=image, dark_image=image,
                                                size=(filtered_image_width, filtered_image_height))
    filtered_image_label = customtkinter.CTkLabel(self, image=filtered_image_ctk, text="")
    filtered_image_label.grid(column=CENTER_COLUMN)
    display_save_and_download_buttons(self)

def display_save_and_download_buttons(self):
    save_image_button = customtkinter.CTkButton(self, text="Save Image", command=save_image)
    download_image_button = customtkinter.CTkButton(self, text="Download Image", command=download_image)

    save_image_button.grid(column=1, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")
    save_button_row = save_image_button.grid_info()['row']
    download_image_button.grid(row=save_button_row, column=2, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")

# Display filtering options
def filter_button_event(self, image, filter_selection):
    if filter_selection != filter_button_event.previous_selection:
        match filter_selection:
            case 1:
                edge_detector_button_event(self, image)
            case 2:
                standard_blur_button_event(self, image)
            case 3:
                gaussian_blur_button_event(self, image)
        filter_button_event.previous_selection = filter_selection

filter_button_event.previous_selection = None

def edge_detector_button_event(self, image):
    filtered_image = create_edge_detector(image)
    display_filtered_image(self, filtered_image)

def standard_blur_button_event(self, image):
    filtered_image = create_standard_blur(image)
    display_filtered_image(self, filtered_image)


def gaussian_blur_button_event(self, image):
    filtered_image = create_gaussian_blur(image)
    display_filtered_image(self, filtered_image)


# Display save image button and download image button
def save_image():
    # TODO: implement
    print("saved")

def download_image():
    # TODO: implement
    print("downloaded")
