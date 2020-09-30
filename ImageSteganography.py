import classic
import numpy as np
import sys

from PIL import Image


def messageToBinary(message):
    if type(message) == bytes or type(message) == np.ndarray:
        return "".join([format(i, "08b") for i in message])
    elif type(message) == str:
        return "".join([format(ord(i), "08b") for i in message])
    else:
        raise TypeError("Input type not supported")


class ImageSteganography:
    @staticmethod
    def hide_message(input_choice, input_image, input_message, input_key=""):
        if input_image is None:
            raise ValueError("requires an input image")
        if input_message is None:
            raise ValueError("requires an input message")

        with open(input_message, "rb") as f:
            data = f.read()
        image = Image.open(input_image)

        bin_choice = messageToBinary(input_choice)
        bin_data = messageToBinary(data)
        message = bin_choice + bin_data
        print(message)

        ImageSteganography.lsb_method(image, message, input_key)
        print(image.format)
        image.save("generated.png", "PNG")
        image.close()

    @staticmethod
    def bit_depth(image_type):
        if image_type == "L" or image_type == "P":
            return 1
        elif image_type == "RGB":
            return 3
        elif image_type == "RGBA":
            return 4
        else:
            raise TypeError("Input type not supported")

    @staticmethod
    def payload(input_message, input_bit, input_width, input_height):
        if len(input_message) * 8 > input_bit * input_width * input_height:
            return False
        return True

    @staticmethod
    def lsb_method(input_image, input_message, input_key):
        width, height = input_image.size
        bit_pixel = ImageSteganography.bit_depth(input_image.mode)

        if not ImageSteganography.payload(input_message, bit_pixel, width, height):
            raise TypeError("too many message")

        i = 0
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(input_image.getpixel((x, y)))
                for n in range(0, bit_pixel):
                    if i < len(input_message):
                        pixel[n] = pixel[n] & ~1 | int(input_message[i])
                        i += 1
                input_image.putpixel((x, y), tuple(pixel))

    @staticmethod
    def bpcs_method(image, message, key=""):
        pass


if __name__ == "__main__":

    print("Penyisipan pesan")
    print("  tanpa enkripsi")
    # print("  dengan enkripsi")
    # enc = input()

    print("  metode lsb")
    print("    pixel-pixel sekuensial")
    # print("    pixel-pixel acak")
    # print("  metode bpcs")
    # print("    blok-blok sekuensial")
    # print("    blok-blok acak")

    # print("ekstraksi pesan")
    # print("  metode lsb")
    # print("  metode bpcs")

    input_choice = input()
    if input_choice[0] == "1":
        if input_choice[1] == "1":
            ImageSteganography.hide_message(input_choice, "save.png", "a.txt", "didik")
    pass
