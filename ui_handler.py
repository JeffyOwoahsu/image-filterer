import tkinter
import customtkinter
from PIL import Image

# Creates window
app = customtkinter.CTk()
app.geometry("400x400")
app.title("Image Filterer")
for i in range(3):
    app.grid_columnconfigure(i, weight=1)

APP_FONT = "Roboto"

# Display main header
TITLE_SIZE = 24
TITLE_ROW = 0
title_label = customtkinter.CTkLabel(app, text="Image Filterer", font=(APP_FONT, TITLE_SIZE))
title_label.grid(row=TITLE_ROW, column=0)

# Display examples
SUBHEADING_SIZE = 16
explanation = customtkinter.CTkLabel(app, text="Upload an image and choose a filter to modify the image.", font=(APP_FONT, SUBHEADING_SIZE))
explanation.grid()

example = customtkinter.CTkLabel(app, text="Example", font=(APP_FONT, SUBHEADING_SIZE - 2))
example.grid()
example_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg")
example_width, example_height = example_image.size
example_image_ctk = customtkinter.CTkImage(light_image=example_image, dark_image=example_image, size=(example_width, example_height))
example_image_label = customtkinter.CTkLabel(app, image=example_image_ctk, text="")
#example_image_label.grid()

# Upload image button
def upload_new_image():
    # TODO: implement
    print("Test")

upload_image_button = customtkinter.CTkButton(app, text="Upload image", command=upload_new_image())
#upload_image_button.grid(pady=20)
#UPLOAD_BUTTON_ROW = upload_image_button.grid_info()['row']

# The following components depend on if an image is successfully updated

# Display uploaded image
# TODO: uploaded image is dependant on the file that is uploaded
image_filename = "d5m0yyl-279d77c8-dfbe-49e9-a009-63e87664d23a.png" # return value will be stored here
if image_filename != "":
    uploaded_image = Image.open(image_filename)
    width, height = uploaded_image.size
    uploaded_image_ctk = customtkinter.CTkImage(light_image=uploaded_image, dark_image=uploaded_image, size=(width,height))
    image_label = customtkinter.CTkLabel(app, image=uploaded_image_ctk, text="")
    #image_label.grid()

# Display filtering options
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

RADIO_PADX, RADIO_PADY = 10, 10

# TODO: fix positioning issue
edge_detector_button.grid(column=0)
RADIO_BUTTON_ROW = edge_detector_button.grid_info()['row']
standard_blur_button.grid(row=RADIO_BUTTON_ROW, column=1)
gaussian_blur_button.grid(row=RADIO_BUTTON_ROW, column=2)

# Display filtered image
# TODO: setting filtered image as a result of convolution
filtered_image = Image.open("456a3ef5ad740d98ff78fab775c69c98.jpg") # Returned image will be stored here
filtered_image_width, filtered_image_height = filtered_image.size
filtered_image_ctk = customtkinter.CTkImage(light_image=filtered_image, dark_image=filtered_image, size=(filtered_image_width, filtered_image_height))
filtered_image_label = customtkinter.CTkLabel(app, image=filtered_image_ctk, text="")

# Display save image button and download image button

# TODO: implement

# Saved images database

# TODO: implement


app.mainloop()