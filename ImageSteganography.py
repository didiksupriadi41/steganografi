import classic
import numpy as np
import sys

from PIL import Image


def messageToBinary(message):
    if type(message) == str:
        return "".join([format(ord(i), "08b") for i in message])
    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]
    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported")


class ImageSteganography:
    @staticmethod
    def bit_depth(image_type):
        if image_type == 'L' or image_type == 'P':
            print("L")
            bit_pixel = 8
        elif image_type == 'RGB':
            print("RGB")
            bit_pixel = 24
        elif image_type == 'RGBA':
            print("RGBA")
            bit_pixel = 32
        else:
            raise TypeError("Input type not supported")
        return bit_pixel

    @staticmethod
    def hide_message(input_image, input_message, input_key=''):
        if input_image is None:
            raise ValueError("requires an input image")
        if input_message is None:
            raise ValueError("requires an input message")

        image = Image.open(input_image)
        bit_pixel = ImageSteganography.bit_depth(image.mode)
        data = open(input_message, "rb")
        message = data.read()
        print(message)
        print(messageToBinary(message))
        ImageSteganography.lsb_method(image, message, input_key)
        image.save("generated.png", "PNG")

    @staticmethod
    def lsb_method(image, message, key=''):
        i = 0
        width, height = image.size
        for x in range(0, width):
            for y in range(0, height):
                pixel = list(image.getpixel((x, y)))
                for n in range(0, 3):
                    if i < len(message):
                        pixel[n] = pixel[n] & ~1 | int(message[i])
                        i += 1
                image.putpixel((x, y), tuple(pixel))

    @staticmethod
    def bpcs_method(image, message, key=''):
        pass


if __name__ == "__main__":
    ImageSteganography.hide_message("a.png", "a.txt", "didik")
    pass
