import classic
import math
import numpy as np
import sys

from PIL import Image
from bpcs.bpcs_steg_encode import encode
from bpcs.bpcs_steg_decode import decode

def messageToBinary(message):
    if type(message) == bytes or type(message) == np.ndarray:
        return "".join([format(i, "08b") for i in message])
    elif type(message) == str:
        return "".join([format(ord(i), "08b") for i in message])
    else:
        raise TypeError("Input type not supported")


class ImageSteganography:
    @staticmethod
    def hide_message(input_choice, input_image, input_message, input_key=''):
        if input_image is None:
            raise ValueError("requires an input image")
        if input_message is None:
            raise ValueError("requires an input message")

        with open(input_message, "r") as f:
            data = f.read()

        image = Image.open(input_image)

        if input_key != '':
            data = classic.ExtendedVigenere.encrypt(data, input_key)

        if input_choice[0] == '1':
            print(1)
            if input_choice[1] == '1':
                print(1)
            elif input_choice[1] == '2':
                print(2)
        elif input_choice[0] == '2':
            print(2)
            if input_choice[1] == '1':
                print(1)
            elif input_choice[1] == '2':
                print(2)

        bin_choice = messageToBinary(input_choice)
        bin_data_len = messageToBinary(str(len(data)))
        print(bin_data_len)

        bin_data = messageToBinary(data)
        message = bin_choice + bin_data
        print(message)

        if input_choice[0] == '1':
            ImageSteganography.lsb_encode(image, message)
        if input_choice[0] == '2':
            ImageSteganography.bpcs_encode(input_image, input_message, '')

        print(image.format)
        if image.format == 'BMP':
            image.save('generated.bmp', 'BMP')
        elif image.format == 'PNG':
            image.save('generated.png', 'PNG')

        original_image = Image.open(input_image)
        stego_image = image

        ImageSteganography.psnr(original_image, stego_image)

        original_image.close()
        image.close()

    @staticmethod
    def show_message(input_image):
        image = Image.open(input_image)
        width, height = image.size

    @staticmethod
    def bit_depth(image_type):
        if image_type == "L" or image_type == "P":
            return 1
        elif image_type == "RGB":
            return 3
        else:
            raise TypeError("Input type not supported")

    @staticmethod
    def payload(input_message, input_bit, input_width, input_height):
        if len(input_message) > input_bit * input_width * input_height:
            return False
        return True

    @staticmethod
    def lsb_encode(input_image, input_message):
        width, height = input_image.size
        bit_depth = ImageSteganography.bit_depth(input_image.mode)

        if not ImageSteganography.payload(input_message, bit_depth, width, height):
            raise ValueError("too many message")

        i = 0
        for x in range(0, width):
            for y in range(0, height):
                if bit_depth == 1:
                    pixel = input_image.getpixel((x, y))
                else:
                    pixel = list(input_image.getpixel((x, y)))

                for n in range(0, bit_depth):
                    if i < len(input_message):
                        if bit_depth == 1:
                            pixel = pixel & ~1 | int(input_message[i])
                        else:
                            pixel[n] = pixel[n] & ~1 | int(input_message[i])
                        i += 1

                if bit_depth == 1:
                    input_image.putpixel((x, y), pixel)
                else:
                    input_image.putpixel((x, y), tuple(pixel))

    @staticmethod
    def bpcs_encode(input_image, input_message, input_key):
        encode(input_image, input_message, 'generated.png', 0.3)

    @staticmethod
    def psnr(input_image, output_image):
        width, height = input_image.size
        bit_depth = ImageSteganography.bit_depth(input_image.mode)
        
        if bit_depth == 1:
            result = 0
        else:
            result_r = 0
            result_g = 0
            result_b = 0

        i = 0
        j = 0
        for i in range(0, width):
            for j in range(0, height):
                if bit_depth == 1:
                    pixel_in = input_image.getpixel((i, j))
                    pixel_out = output_image.getpixel((i, j))
                    result = result + (float(pixel_in) - float(pixel_out)) ** 2
                else:
                    pixel_in = list(input_image.getpixel((i, j)))
                    pixel_out = list(output_image.getpixel((i, j)))
                    result_r = result_r + (float(pixel_in[0]) - float(pixel_out[0])) ** 2
                    result_g = result_g + (float(pixel_in[1]) - float(pixel_out[1])) ** 2
                    result_b = result_b + (float(pixel_in[2]) - float(pixel_out[2])) ** 2

        if bit_depth == 3:
            result = (result_r + result_g + result_b) / 3

        result = math.sqrt(result / (width * height))
        psnr_value = 20 * math.log10(255 / result)

        print(psnr_value)
        if psnr_value >= 30:
            print('good image quality')
        elif psnr_value < 30:
            print('significant degraded image quality')

if __name__ == "__main__":

    print("Penyisipan pesan")
    print("  tanpa enkripsi")
    print("  dengan enkripsi")
    # enc = input()

    print("  metode lsb")
    print("    pixel-pixel sekuensial")
    # print("    pixel-pixel acak")
    print("  metode bpcs")
    # print("    blok-blok sekuensial")
    # print("    blok-blok acak")

    print("ekstraksi pesan")
    # print("  metode lsb")
    # print("  metode bpcs")

    input_choice = input()
    if input_choice[0] == '1':
        ImageSteganography.hide_message(input_choice, 'bank.png', 'a.txt', 'didik')
    elif input_choice[0] == '2':
        ImageSteganography.bpcs_encode('bank.png', 'a.txt', 'didik')
    pass
