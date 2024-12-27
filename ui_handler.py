import tkinter

import customtkinter
from customtkinter import filedialog
from PIL import Image

from io_handler import validate_image

APP_FONT = "Roboto"
TITLE_SIZE = 24
SUBHEADING_SIZE = 16
CENTER_COLUMN = 1
BUTTON_PADX, BUTTON_PADY = 5, 5

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
        self.example_image_label.grid(column=CENTER_COLUMN)

        # Create upload image button
        self.upload_image_label = customtkinter.CTkLabel(self, text="Upload an image (.png & .jpeg accepted)", font=(APP_FONT, SUBHEADING_SIZE - 2))
        self.upload_image_label.grid(column=CENTER_COLUMN)
        self.upload_image_button = customtkinter.CTkButton(self, text="Upload image", command=upload_new_image)
        self.upload_image_button.grid(column=CENTER_COLUMN, pady=5)
        self.UPLOAD_BUTTON_ROW = self.upload_image_button.grid_info()['row']

        # TODO: The following components depend on if an image is successfully updated

        # Display uploaded image
        # TODO: uploaded image is dependant on the file that is uploaded
        image_filename = "d5m0yyl-279d77c8-dfbe-49e9-a009-63e87664d23a.png"  # return value will be stored here
        if image_filename != "":
            uploaded_image = Image.open(image_filename)
            window_width, window_height = uploaded_image.size
            uploaded_image_ctk = customtkinter.CTkImage(light_image=uploaded_image, dark_image=uploaded_image,
                                                        size=(window_width, window_height))
            image_label = customtkinter.CTkLabel(self, image=uploaded_image_ctk, text="")
            # image_label.grid(column=CENTER_COLUMN)

        selected_filter = tkinter.IntVar(value=0)
        edge_detector_button = customtkinter.CTkRadioButton(self, text="Edge Detector",
                                                            command=edge_detector_button_event,
                                                            variable=selected_filter, value=1)
        standard_blur_button = customtkinter.CTkRadioButton(self, text="Standard Blur",
                                                            command=standard_blur_button_event,
                                                            variable=selected_filter, value=2)
        gaussian_blur_button = customtkinter.CTkRadioButton(self, text="Gaussian Blur",
                                                            command=gaussian_blur_button_event,
                                                            variable=selected_filter, value=3)

        edge_detector_button.grid(column=0, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="e")
        radio_button_row = edge_detector_button.grid_info()['row']
        standard_blur_button.grid(column=1, row=radio_button_row, padx=BUTTON_PADX, pady=BUTTON_PADY)
        gaussian_blur_button.grid(column=2, row=radio_button_row, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")

        # Display filtered image
        # TODO: setting filtered image as a result of convolution
        filtered_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg")  # Returned image will be stored here
        filtered_image_width, filtered_image_height = filtered_image.size
        filtered_image_ctk = customtkinter.CTkImage(light_image=filtered_image, dark_image=filtered_image,
                                                    size=(filtered_image_width, filtered_image_height))
        filtered_image_label = customtkinter.CTkLabel(self, image=filtered_image_ctk, text="")
        # filtered_image_label.grid(column=CENTER_COLUMN)

        # Save and download buttons
        save_image_button = customtkinter.CTkButton(self, text="Save Image", command=save_image)
        download_image_button = customtkinter.CTkButton(self, text="Download Image", command=download_image)

        save_image_button.grid(column=1, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")
        save_button_row = save_image_button.grid_info()['row']
        download_image_button.grid(row=save_button_row, column=2, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")

        # Saved images database
        # TODO: implement; have it so that it dynamically changes rows
        saved_images_label = customtkinter.CTkLabel(self, text="Saved Images", font=(APP_FONT, SUBHEADING_SIZE))
        saved_images_label.grid(column=CENTER_COLUMN)


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
# Supported files are JPEG and PNG
def upload_new_image():
    filepath = filedialog.askopenfile().name
    if validate_image(filepath):
        print("yay")
    else:
        print("nuh uh")


# Display filtering options
# Make sure these functions are only called once
def edge_detector_button_event():
    # TODO: implement
    print("radiobutton toggled, edge detector:")

def standard_blur_button_event():
    # TODO: implement
    print("radiobutton toggled, standard blur:")

def gaussian_blur_button_event():
    # TODO: implement
    print("radiobutton toggled, gaussian blur:")

# Display save image button and download image button
def save_image():
    # TODO: implement
    print("saved")

def download_image():
    # TODO: implement
    print("downloaded")
