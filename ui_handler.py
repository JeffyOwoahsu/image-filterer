import tkinter
from tkinter.constants import CENTER

import io

import customtkinter
from customtkinter import filedialog
from PIL import Image

from io_handler import validate_image, convert_json_to_image, convert_image_to_json
from filter_generator import create_edge_detector, create_standard_blur, create_gaussian_blur
from database_driver import initialize_database, insert_image_to_database, retrieve_image_from_database, get_number_of_images

APP_FONT = "Roboto"
TITLE_SIZE = 24
SUBHEADING_SIZE = 16
POPUP_SIZE = 14
CENTER_COLUMN = 0 # must be used with columnspan = 3
BUTTON_PADX, BUTTON_PADY = 5, 5
selected_filter = 0

# Global variables
image_uploaded = False
uploaded_image_spawn_row = None
filtered_image_displayed = False
filtered_image_spawn_row = None

class MyFrame(customtkinter.CTkScrollableFrame):
    def _on_mousewheel(self, event):
        scroll_speed = -45
        self._parent_canvas.yview_scroll(int(scroll_speed * (event.delta / 120)), "units")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure((0, 1, 2), weight=1, uniform='a')

        # Configure mousewheel speed
        self.bind_all('<MouseWheel>', self._on_mousewheel)

        # Create title
        self.title_label = customtkinter.CTkLabel(self, text="Image Filterer", font=(APP_FONT, TITLE_SIZE))
        self.title_label.grid(column=CENTER_COLUMN, sticky="n", columnspan=3)

        # Create explanation
        self.explanation = customtkinter.CTkLabel(self, text="Upload an image and choose a filter to modify the image.",
                                             font=(APP_FONT, SUBHEADING_SIZE))
        self.explanation.grid(column=CENTER_COLUMN, sticky="ew", columnspan=3)

        # self.example = customtkinter.CTkLabel(self, text="Example", font=(APP_FONT, SUBHEADING_SIZE))
        # self.example.grid(column=CENTER_COLUMN)
        # self.example_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg")
        # self.example_width, example_height = self.example_image.size
        # self.example_image_ctk = customtkinter.CTkImage(light_image=self.example_image, dark_image=self.example_image,
        #                                            size=(self.example_width, example_height))
        # self.example_image_label = customtkinter.CTkLabel(self, image=self.example_image_ctk, text="")
        # #self.example_image_label.grid(column=CENTER_COLUMN)

        # Create upload image button
        self.upload_image_label = customtkinter.CTkLabel(self, text="Upload an image (.png & .jpeg accepted)", font=(APP_FONT, SUBHEADING_SIZE - 2))
        self.upload_image_label.grid(column=CENTER_COLUMN, columnspan=3)
        self.upload_image_button = customtkinter.CTkButton(self, text="Upload image", command=lambda: upload_new_image(self))
        self.upload_image_button.grid(column=CENTER_COLUMN, pady=5, columnspan=3)
        self.UPLOAD_BUTTON_ROW = self.upload_image_button.grid_info()['row']

        # Saved images database
        initialize_database()
        display_save_images(self)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.grid_columnconfigure((0,1,2), weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1)
        window_width = self.winfo_screenwidth()
        window_height = self.winfo_screenwidth()
        self.geometry(f"{window_width}x{window_height}+0+0")
        self.my_frame = MyFrame(master=self, width=window_width, height=window_height, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")


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
    global image_uploaded, uploaded_image_spawn_row
    image_filename = filepath
    uploaded_image = Image.open(image_filename)
    # TODO: show a scaled down version of the image
    window_width, window_height = uploaded_image.size
    uploaded_image_ctk = customtkinter.CTkImage(light_image=uploaded_image, dark_image=uploaded_image,
                                                    size=(window_width, window_height))
    image_label = customtkinter.CTkLabel(self, image=uploaded_image_ctk, text="")
    if not image_uploaded:
        image_label.grid(column=CENTER_COLUMN, columnspan=3)
        uploaded_image_spawn_row = image_label.grid_info()['row']
        image_uploaded = True
    else:
        for widget in self.grid_slaves():
            if widget.grid_info()['row'] == uploaded_image_spawn_row:
                widget.destroy()
                break
            image_label.grid(row=uploaded_image_spawn_row, column=CENTER_COLUMN, columnspan=3)
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
    global filtered_image_spawn_row, filtered_image_displayed
    should_grid_buttons = None
    filtered_image_width, filtered_image_height = image.size
    filtered_image_ctk = customtkinter.CTkImage(light_image=image, dark_image=image,
                                                size=(filtered_image_width, filtered_image_height))
    filtered_image_label = customtkinter.CTkLabel(self, image=filtered_image_ctk, text="")
    if not filtered_image_displayed:
        filtered_image_label.grid(column=CENTER_COLUMN, columnspan=3)
        filtered_image_spawn_row = filtered_image_label.grid_info()['row']
        filtered_image_displayed = True
        should_grid_buttons = True
    else:
        for widget in self.grid_slaves():
            if widget.grid_info()['row'] == filtered_image_spawn_row:
                widget.destroy()
                break
        filtered_image_label.grid(row=filtered_image_spawn_row, column=CENTER_COLUMN, columnspan=3)
        should_grid_buttons = False
    display_save_and_download_buttons(self, image, should_grid_buttons)

def display_save_and_download_buttons(self, image, should_grid):
    save_image_button = customtkinter.CTkButton(self, text="Save Image", command=lambda:save_image(image))
    download_image_button = customtkinter.CTkButton(self, text="Download Image", command=filedialog.asksaveasfilename)
    if should_grid:
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
            case _:
                raise Exception("An error has occurred.")
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
def save_image(image):
    dialog = customtkinter.CTkInputDialog()
    image_name = dialog.get_input()
    if image_name is None:
        raise Exception("User pressed cancel.")
    image_data = convert_image_to_json(image)
    insert_image_to_database(image_data, image_name)

def display_save_images(self):
    num_of_images = get_number_of_images()
    if num_of_images == 0:
        return
    else:
        saved_images_label = customtkinter.CTkLabel(self, text="Saved Images", font=(APP_FONT, SUBHEADING_SIZE))
        saved_images_label.grid(column=CENTER_COLUMN, columnspan=3)
        for image_id in range(1, num_of_images + 1):
            image_data, image_name = retrieve_image_from_database(image_id)
            image = convert_json_to_image(image_data)

            image_width, image_height = image.size
            image_ctk = customtkinter.CTkImage(light_image=image, dark_image=image, size=(image_width, image_height))
            image_label = customtkinter.CTkLabel(self, image=image_ctk, text="")
            image_name_label = customtkinter.CTkLabel(self, text=image_name, font=(APP_FONT, SUBHEADING_SIZE))

            image_name_label.grid(column=CENTER_COLUMN, columnspan=3)
            image_label.grid(column=CENTER_COLUMN, columnspan=3)