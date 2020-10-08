import classic
import math
import numpy as np
import sys
import random

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
    def hide_message(input_choice, input_image, input_message, input_key="", output_image="output.png", pixelSequential=True, from_file=False, encrypt=False):
        if input_image is None:
            raise ValueError("requires an input image")
        if input_message is None:
            raise ValueError("requires an input message")

        if from_file == True:
            with open(input_message, "r") as f:
                input_message = f.read()

        image = Image.open(input_image)

        if encrypt:
            input_message = classic.ExtendedVigenere.encrypt(input_message, input_key)

        if pixelSequential:
            input_message = "1" + input_message
        else:
            input_message = "2" + input_message

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
        bin_input_message_len = messageToBinary(str(len(input_message)))
        print(bin_input_message_len)

        bin_input_message = messageToBinary(input_message)
        message = bin_choice + bin_input_message
        print(message)

        if input_choice[0] == '1':
            image = ImageSteganography.encodeLSB(image, input_message, input_key=input_key, output_image=output_image, pixelSequential=pixelSequential)
        if input_choice[0] == '2':
            ImageSteganography.bpcs_encode(input_image, input_message, '')

        print(image.format)
        image.save(output_image)
        # if image.format == 'BMP':
        #     image.save('generated.bmp', 'BMP')
        # elif image.format == 'PNG':
        #     image.save('generated.png', 'PNG')

        original_image = Image.open(input_image)
        stego_image = image

        #ImageSteganography.psnr(original_image, stego_image)

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
    def embedBitsToPixels(binaryNTuple, pixels):
        print("embedBitsToPixels")
        print(binaryNTuple)
        binaryAllPixelsList = []
        for pixel in pixels:
            binaryPixelList=[]
            for p in pixel:
                binaryPixel = bin(p)[2:].rjust(8,'0')
                binaryPixelList.append(binaryPixel)
            binaryAllPixelsList.append(binaryPixelList)
        for i in range(len(binaryNTuple)):
            for j in range(len(binaryNTuple[i])):
                binaryAllPixelsList[i][j] = list(binaryAllPixelsList[i][j])
                binaryAllPixelsList[i][j][-1] = binaryNTuple[i][j]
                binaryAllPixelsList[i][j] = "".join(binaryAllPixelsList[i][j])
        newPixelsTupleList = []
        newPixelsTuple = ()
        for pixel in binaryAllPixelsList:
            newPixelsTupleList.append(tuple(int(p,2) for p in pixel))
        return newPixelsTupleList

    @staticmethod
    def createBinaryNTupleList(message, bit_depth, key):
        binariesList = []
        method_code = message[0]
        print("method_code = ", method_code, " , type = ", type(method_code))
        print("message createBinary = ", message)
        print("message len = ", len(message))
        #process message after method code
        if (len(message)-1) > 0:
            for i in range(1,len(message)):
                binaries = bin(ord(message[i]))[2:].rjust(8,'0')
                #print("message[i] = ", message[i], "binaries = ", binaries)
                binariesList.append(binaries)
            
            print("current binariesList createBinary = ", binariesList)
            #If not pixelSequential
            print("method_code before shuffle = ", method_code)
            if method_code != "1":
                print("not pixelSequential")
                #shuffle list
                seed = ImageSteganography.calculate_seed(key)
                #print("seed encode = ", seed)
                random.seed(seed)
                print("binariesList = ", binariesList)
                #method_code_binary = binariesList[0]
                #binariesList = binariesList[1:]
                random.shuffle(binariesList)
                print("shuffledBinariesList = ", binariesList)
                #binariesList.insert(0, method_code_binary)
                binary = bin(ord(method_code))[2:].rjust(8,'0')
                #Append Method Code
                binariesList.insert(0, binary)
                print("current binariesList createBinary after shuffle & insert method_code= ", binariesList)
            else:
                print("pixelSequential")
                # #binariesList.append(method_code)
                # #print("ord(1) = ", ord("1"))
                # #print("ord(method_code = ", ord(method_code))
                # #print("bin ord method_code = ", bin(ord(method_code))[2:])
                binary = bin(ord(method_code))[2:].rjust(8,'0')
                # #print("binary = ", binary)
                binariesList.insert(0, binary)
                pass

        expectedbinariesList = []
        for i in range(len(message)):
            expected_binaries = bin(ord(message[i]))[2:].rjust(8,'0')
            expectedbinariesList.append(expected_binaries)
        #Combine List into String
        print("binariesList = ", binariesList)
        print("is it equal to expected result? = ", binariesList == expectedbinariesList)
        binariesString = "".join(binariesList)
        #print("binariesString = ", binariesString)
        binariesStringList = list(binariesString)
        #binariesList.append(binariesStringList)
        #print("binaries #1 = ", binariesStringList)
        #Append stop bits
        for i in range(8):
            binariesStringList.append('0')
        #print("binaries #2 = ", binariesStringList)
        #Append missing bits to make pixel
        binariesStringList = binariesStringList + ['0'] * (len(binariesStringList) % bit_depth)
        #print("binaries #3 = ", binariesStringList)
        newBinariesList = []
        for i in range(0,int(len(binariesStringList) / bit_depth)):
                newBinariesList.append(binariesStringList[i*bit_depth:i*bit_depth+bit_depth])
        print("binaries #4 = ", newBinariesList)
        return newBinariesList

    @staticmethod
    def calculate_seed(key):
        seed = 0
        for character in key:
            seed += ord(character)
        return seed
    
    @staticmethod
    def encodeLSB(input_image, input_message, input_key="", steganographyMethod="", output_image="output.png", pixelSequential=True):
        #print("PixelSequential = ", pixelSequential)
        size = input_image.size
        width, height = size
        bit_depth = ImageSteganography.bit_depth(input_image.mode)
        newImg = Image.new(input_image.mode, size)
            
        print("input_message encodeLSB = ", input_message)
        if input_message == '':
            return input_image

        #print("pixelSequential = ", pixelSequential)
        if not pixelSequential:

            pass
        
        print("input_message = ", input_message)
        
        if not ImageSteganography.payload(input_message, bit_depth, width, height):
                return None

        binaryTriplePairs = ImageSteganography.createBinaryNTupleList(input_message, bit_depth, input_key)
        #binaryTriplePairs = createBinaryTriplePairs(message)
        print("binaryTriplePairs = ", binaryTriplePairs)


        pixels = list(input_image.getdata())
        #print("pixels = ", pixels)
            
        newPixels = ImageSteganography.embedBitsToPixels(binaryTriplePairs, pixels)

        print("putting data")
        newImg.putdata(newPixels)
        #print("newPixels = ", newPixels)
        
        print("putdata finished")

        return newImg

    @staticmethod
    def getLSBsFromPixels(binaryPixels):
        totalZeros = 0
        binList = []
        for binaryPixel in binaryPixels:
            for p in binaryPixel:
                if p[-1] == '0':
                    totalZeros = totalZeros + 1
                else:
                        totalZeros = 0
                binList.append(p[-1])
                if totalZeros == 8:
                        return binList

    @staticmethod
    def shuffle_under_seed(ls, seed):
        # Shuffle the list ls using the seed `seed`
        random.seed(seed)
        random.shuffle(ls)
        return ls

    @staticmethod
    def unshuffle_list(shuffled_ls, seed):
        n = len(shuffled_ls)
        # Perm is [1, 2, ..., n]
        perm = [i for i in range(1, n + 1)]
        # Apply sigma to perm
        random.seed(seed)
        random.shuffle(perm)
        shuffled_perm = perm
        # Zip and unshuffle
        zipped_ls = list(zip(shuffled_ls, shuffled_perm))
        zipped_ls.sort(key=lambda x: x[1])
        return [a for (a, b) in zipped_ls]

    @staticmethod
    def decodeLSB(imageFilename, key):
        print("decode LSB ImageSteganography")
        img = Image.open(imageFilename)
        pixels = list(img.getdata())
        binaryAllPixelsList = []
        for pixel in pixels:
            binaryPixelList=[]
            for p in pixel:
                binaryPixel = bin(p)[2:].rjust(8,'0')
                binaryPixelList.append(binaryPixel)
            binaryAllPixelsList.append(binaryPixelList)
        #print("Decode binaryPixelList = ",binaryAllPixelsList)
        binList = ImageSteganography.getLSBsFromPixels(binaryAllPixelsList)
        print("Decode binList", binList)
        message_list = []
        message_char = ""
        if len(binList) > 0:
            for i in range(0,len(binList)-8,8):
                message_char = chr(int("".join(binList[i:i+8]),2))
                message_list.append(message_char)
        print("current messagelist before trim= ", message_list)
        #cut method code from message list
        message = ""
        #message_list = message_list[1:]
        print("current messagelist = ", message_list)
        if len(message_list) > 0:
            print("current messagelist check= ", message_list)
            if message_list[0] == "2":
                print("message_list before unshuffle= ",message_list)
                message_list = message_list[1:]
                print("message_list before unshuffle, after removal of method_code = ",message_list)
                seed = ImageSteganography.calculate_seed(key)
                print("seed decode = ", seed)
                message_list = ImageSteganography.unshuffle_list(message_list, seed)
            else:
                #cut method_code from message
                message_list = message_list[1:]
            message = "".join(message_list)
        return message

    # @staticmethod
    # def lsb_encode(input_image, input_message):
    #     width, height = input_image.size
    #     bit_depth = ImageSteganography.bit_depth(input_image.mode)

    #     if not ImageSteganography.payload(input_message, bit_depth, width, height):
    #         raise ValueError("too many message")

    #     i = 0
    #     for x in range(0, width):
    #         for y in range(0, height):
    #             if bit_depth == 1:
    #                 pixel = input_image.getpixel((x, y))
    #             else:
    #                 pixel = list(input_image.getpixel((x, y)))

    #             for n in range(0, bit_depth):
    #                 if i < len(input_message):
    #                     if bit_depth == 1:
    #                         pixel = pixel & ~1 | int(input_message[i])
    #                     else:
    #                         pixel[n] = pixel[n] & ~1 | int(input_message[i])
    #                     i += 1

    #             if bit_depth == 1:
    #                 input_image.putpixel((x, y), pixel)
    #             else:
    #                 input_image.putpixel((x, y), tuple(pixel))

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
        ImageSteganography.hide_message(input_choice, "save.png", "a.txt", input_key="didik", output_image="generated.png", pixelSequential=False, from_file=True, encrypt=False)
        print("message = ", ImageSteganography.decodeLSB("generated.png", key="didik"))
    elif input_choice[0] == '2':
        ImageSteganography.bpcs_encode('bank.png', 'a.txt', 'didik')
    pass
