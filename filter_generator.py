import numpy as np
from PIL import Image
from scipy.fftpack import fft2, ifft2, fftshift

def create_edge_detector(image):
    # Create greyscale version of the image
    greyscale = image.convert("L")

    # Apply the Fast Fourier Transform (FFT) on the image
    image_array = np.array(greyscale, dtype=np.float32)
    image_fft = fft2(image_array)

    # Create x and y kernels and apply FFT on them
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]], dtype=np.float32)
    kernel_y = np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]], dtype=np.float32)

    # Pad the kernels to the size of the image
    padded_kernel_x = np.zeros_like(image_array)
    padded_kernel_y = np.zeros_like(image_array)
    kx_h, kx_w = kernel_x.shape
    ky_h, ky_w = kernel_y.shape
    padded_kernel_x[:kx_h, :kx_w] = kernel_x
    padded_kernel_y[:ky_h, :ky_w] = kernel_y

    # Apply FFT on the kernels
    kernel_x_fft = fft2(padded_kernel_x)
    kernel_y_fft = fft2(padded_kernel_y)

    # Convolve in the frequency domain (multiplication)
    result_x_fft = image_fft * kernel_x_fft
    result_y_fft = image_fft * kernel_y_fft

    # Transform back to spatial domain
    result_x = np.abs(ifft2(result_x_fft))
    result_y = np.abs(ifft2(result_y_fft))

    # Compute the magnitude and normalize it
    edge_magnitude = np.sqrt(result_x ** 2 + result_y ** 2)

    return Image.fromarray(edge_magnitude)

def create_standard_blur(image):
    print()

def create_gaussian_blur(image):
    print()