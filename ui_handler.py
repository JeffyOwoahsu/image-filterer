import tkinter
from random import uniform

import customtkinter
from PIL import Image

APP_FONT = "Roboto"

# Creates window
app = customtkinter.CTk()
app.geometry("400x400")
app.title("Image Filterer")
app.columnconfigure((0,1,2), weight=1, uniform='a')
CENTER_COLUMN = 1

# TODO: implement scrollbar

# Display main header
TITLE_SIZE = 24
TITLE_ROW = 0
title_label = customtkinter.CTkLabel(app, text="Image Filterer", font=(APP_FONT, TITLE_SIZE))
title_label.grid(column=CENTER_COLUMN)

# Display examples
SUBHEADING_SIZE = 16
explanation = customtkinter.CTkLabel(app, text="Upload an image and choose a filter to modify the image.", font=(APP_FONT, SUBHEADING_SIZE))
explanation.grid(column=0, columnspan=3, sticky="ew")

example = customtkinter.CTkLabel(app, text="Example", font=(APP_FONT, SUBHEADING_SIZE))
example.grid(column=CENTER_COLUMN)
example_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg")
example_width, example_height = example_image.size
example_image_ctk = customtkinter.CTkImage(light_image=example_image, dark_image=example_image, size=(example_width, example_height))
example_image_label = customtkinter.CTkLabel(app, image=example_image_ctk, text="")
#example_image_label.grid(column=1)

# Upload image button
def upload_new_image():
    # TODO: implement
    print("Test")

upload_image_button = customtkinter.CTkButton(app, text="Upload image", command=upload_new_image)
upload_image_button.grid(column=CENTER_COLUMN, pady=5)
UPLOAD_BUTTON_ROW = upload_image_button.grid_info()['row']

# TODO: The following components depend on if an image is successfully updated

# Display uploaded image
# TODO: uploaded image is dependant on the file that is uploaded
image_filename = "d5m0yyl-279d77c8-dfbe-49e9-a009-63e87664d23a.png" # return value will be stored here
if image_filename != "":
    uploaded_image = Image.open(image_filename)
    width, height = uploaded_image.size
    uploaded_image_ctk = customtkinter.CTkImage(light_image=uploaded_image, dark_image=uploaded_image, size=(width,height))
    image_label = customtkinter.CTkLabel(app, image=uploaded_image_ctk, text="")
    #image_label.grid(column=CENTER_COLUMN)

# Display filtering options
# Make sure these functions are only called once
def edge_detector_button_event():
    # TODO: implement
    print("radiobutton toggled, current value:", selected_filter.get())

def standard_blur_button_event():
    # TODO: implement
    print("radiobutton toggled, current value:", selected_filter.get())

def gaussian_blur_button_event():
    # TODO: implement
    print("radiobutton toggled, current value:", selected_filter.get())

selected_filter = tkinter.IntVar(value=0)
edge_detector_button = customtkinter.CTkRadioButton(app, text="Edge Detector",
                                                    command=edge_detector_button_event, variable= selected_filter, value=1)
standard_blur_button = customtkinter.CTkRadioButton(app, text="Standard Blur",
                                                    command=standard_blur_button_event, variable= selected_filter, value=2)
gaussian_blur_button = customtkinter.CTkRadioButton(app, text="Gaussian Blur",
                                                    command=gaussian_blur_button_event, variable= selected_filter, value=3)

BUTTON_PADX, BUTTON_PADY = 5, 5

# TODO: fix positioning issue
edge_detector_button.grid(column=0, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="e")
RADIO_BUTTON_ROW = edge_detector_button.grid_info()['row']
standard_blur_button.grid(column=1, row=RADIO_BUTTON_ROW, padx=BUTTON_PADX, pady=BUTTON_PADY)
gaussian_blur_button.grid(column=2, row=RADIO_BUTTON_ROW, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="w")

# Display filtered image
# TODO: setting filtered image as a result of convolution
filtered_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg") # Returned image will be stored here
filtered_image_width, filtered_image_height = filtered_image.size
filtered_image_ctk = customtkinter.CTkImage(light_image=filtered_image, dark_image=filtered_image, size=(filtered_image_width, filtered_image_height))
filtered_image_label = customtkinter.CTkLabel(app, image=filtered_image_ctk, text="")
#filtered_image_label.grid(column=CENTER_COLUMN)

# Display save image button and download image button
def save_image():
    # TODO: implement
    print("saved")

def download_image():
    # TODO: implement
    print("downloaded")

save_image_button = customtkinter.CTkButton(app, text="Save Image", command=save_image)
download_image_button = customtkinter.CTkButton(app, text="Download Image", command=download_image)
save_image_button.grid(column=0, padx=BUTTON_PADX, pady=BUTTON_PADY, sticky="e")
SAVE_BUTTON_ROW = save_image_button.grid_info()['row']
download_image_button.grid(row=SAVE_BUTTON_ROW, column=1, padx=BUTTON_PADX, pady=BUTTON_PADY)

# Saved images database
saved_images_label = customtkinter.CTkLabel(app, text="Saved Images", font=(APP_FONT, SUBHEADING_SIZE))
saved_images_label.grid(column=CENTER_COLUMN)


app.mainloop()