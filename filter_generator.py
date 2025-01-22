import numpy as np
from PIL import Image
from scipy.fftpack import fft2, ifft2


def create_filter(filter_num, image):
    match filter_num:
        case 1:
            return create_edge_detector(image)
        case 2:
            return create_standard_blur(image)
        case 3:
            return create_sharpen(image)
        case _:
            raise Exception("An image processing error has occurred")

def create_edge_detector(image):
    # Create greyscale version of the image
    greyscale = image.convert("L")

    # Apply the Fast Fourier Transform (FFT) on the image
    image_array = np.array(greyscale, dtype=np.float32)
    image_fft = fft2(image_array)

    # Define x and y kernels
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]], dtype=np.float32)

    # Pad the kernels to the size of the image
    padded_kernel_x = pad_kernel(kernel_x, image_array)
    padded_kernel_y = pad_kernel(kernel_y, image_array)

    # Apply FFT on the kernels
    kernel_x_fft = fft2(padded_kernel_x)
    kernel_y_fft = fft2(padded_kernel_y)

    # Convolve in the frequency domain (multiplication)
    result_x_fft = image_fft * kernel_x_fft
    result_y_fft = image_fft * kernel_y_fft

    # Transform back to spatial domain
    result_x = np.abs(ifft2(result_x_fft))
    result_y = np.abs(ifft2(result_y_fft))

    # Compute the magnitude
    edge_magnitude = np.sqrt(result_x ** 2 + result_y ** 2)

    return Image.fromarray(edge_magnitude)

def create_standard_blur(image):
    kernel = np.array([[1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1],
                       [1, 1, 1, 1]], dtype=np.float32)

    kernel /= kernel.sum() # Normalizes kernel
    return process_channels(image, kernel)

def create_sharpen(image):
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], dtype=np.float32)

    return process_channels(image, kernel)

# Helper Methods
def pad_kernel(kernel, data):
    padded_kernel = np.zeros_like(data)
    k_h, k_w = kernel.shape
    padded_kernel[:k_h, :k_w] = kernel
    return padded_kernel

def process_channels(image, kernel):
    image_array = np.array(image, dtype=np.float32)

    # Process each channel separately
    processed_channels = []
    for channel in range(image_array.shape[2]):  # Assuming the image has 3 channels (RGB)
        channel_data = image_array[:, :, channel]

        # Apply FFT on the channel
        channel_fft = fft2(channel_data)

        # Create padded kernel
        padded_kernel = pad_kernel(kernel, channel_data)

        # Apply FFT on kernel
        kernel_fft = fft2(padded_kernel)

        # Convolve
        result_fft = channel_fft * kernel_fft

        # Transform back to spatial domain
        result = np.abs(ifft2(result_fft))

        processed_channels.append(result.astype(np.uint8))

    # Stack the processed channels back into an image
    processed_image = np.stack(processed_channels, axis=-1)
    return Image.fromarray(processed_image)
