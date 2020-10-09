#videoSteganography
from PIL import Image
import shutil,cv2,os
import classic

#main
from pyfiglet import Figlet
from subprocess import call,STDOUT
import os

#convert frame to video
import numpy as np
import re
import glob

#Image Steganography
import ImageSteganography
import pathlib
import random
import math

def frame_extract(video, output_folder):
    if os.path.exists(output_folder):
        remove(output_folder)
        os.mkdir(output_folder)
    else:
        os.mkdir(output_folder)
    # try:
    #     os.mkdir(output_folder)
    # except OSError or FileExistsError:
    #     remove(output_folder)
    #     os.mkdir(output_folder)
    vidcap = cv2.VideoCapture("data/"+str(video))
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print("fps = ",fps)
    count = 0
    while True:
        success, image = vidcap.read()
        if not success:
            # print("count = ",count)
            # print("NOT SUCCESS")
            break
        cv2.imwrite(os.path.join(output_folder, "{:d}.png".format(count)), image)
        count += 1
    return fps

def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def write_video(output_video, output_folder, fps):
    img_array = []
    print("sorted glob = " ,sorted(glob.glob('./temp/*.png'),key=alphanum_key))
    for filename in sorted(glob.glob('./temp/*.png'),key=alphanum_key):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    #cv2.VideoWriter()
    
    out = cv2.VideoWriter(output_folder + "/" + output_video ,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def remove(path):
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains
    else:
        raise ValueError("file {} is not a file or dir.".format(path))

def splitString(string_to_split, split_length):
    splittedStringList = []
    for i in range (0, len(string_to_split), split_length):
        splittedStringPart = string_to_split[i:i+split_length]
        #print("splittedStringPart = ", splittedStringPart)
        splittedStringList.append(splittedStringPart)
    print("splittedStringList In Method = ", splittedStringList)
    return splittedStringList

def appendMethodCode(string_to_append, length, method_code, frameOrderList):
    appendedStringList = ["" for i in range(len(frameOrderList))]
    frameOrderListIndex = 0
    #print('frameOrderList = ', frameOrderList)
    #input method code
    frameZeroPassed = False
    for i in range (0, len(string_to_append), length):
        if frameOrderList[frameOrderListIndex] == '0':
            frameZeroPassed = True
            splittedStringPart = method_code + string_to_append[i:i+length]
            appendedStringList[frameOrderListIndex] = splittedStringPart
        else:
            splittedStringPart = string_to_append[i:i+length]
            #print("splittedStringPart = ", splittedStringPart)
            appendedStringList[frameOrderListIndex] = splittedStringPart
        frameOrderListIndex += 1
    if not frameZeroPassed:
        #appendedStringList[frameOrderList.index(0)] = method_code + appendedStringList[frameOrderList.index(0)]
        appendedStringList[frameOrderList.index(1)] = method_code + appendedStringList[frameOrderList.index(1)]
    #print("appendedStringList ", appendedStringList)
    return appendedStringList, frameZeroPassed

def toUpperCase(text):
    return "".join(filter(str.isupper, text.upper()))

def decode(frame_dir, input_video, key="", output_message="decodedMessage.txt"):
    call(["ffmpeg", "-i", input_video, frame_dir+"/%d.png", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    seed = calculate_seed(key)
    frameCount = get_frameCount(frame_dir)
    frameOrderList = initialize_frameOrderList(frameCount)
    method_code = "0"
    decodedMessageList = []
    #check code at first frame
    print("decode Method Code = ", method_code)
    for frameName in frameOrderList:
        print("frameName = ", frameName)
        decodedMessagePart = ImageSteganography.ImageSteganography.decodeLSB(str(frame_dir) +"/" + str(frameName) + ".png", key)
        decodedMessageList.append(decodedMessagePart)
        print("decodedMessagePart = ", decodedMessagePart)
    print("decodedMessageList = ", decodedMessageList)
    messageFirstFrame = decodedMessageList[0]
    print("messageFirstFrame = ", messageFirstFrame)
    method_code = messageFirstFrame[:2]
    print("decode Method Code = ", method_code)
    decodedMessageList[0] = decodedMessageList[0][len(method_code):]
    print("decodedMessageList[0] = ", decodedMessageList[0])
    decodedMessage = ""
    if method_code[0] == "4":
        random.seed(seed)
        random.shuffle(frameOrderList)
        print("frameOrderList decode = ", frameOrderList)
        newMessageList = ["" for i in range(len(frameOrderList))]
        print("frameOrderList = ", frameOrderList)
        for i in range(len(frameOrderList)):
            #print("int(frameOrderList[i]) = ", int(frameOrderList[i]), "message = ", messageList[int(frameOrderList[i])])
            newMessageList[i] = decodedMessageList[int(frameOrderList[i])-1]
        print("newMessageList = ",newMessageList)
        decodedMessage = "".join(newMessageList)
        print("newMessage = ", decodedMessage)
    else:
        decodedMessage = "".join(decodedMessageList)
        print("decoded message = " , decodedMessage)
    if method_code[1] == "4":
        #encrypted
        decodedMessage = classic.ExtendedVigenere.decrypt(decodedMessage,key)
    text_file = open(output_message, "w+")
    text_file.write(decodedMessage)
    text_file.close()
    return decodedMessage

def calculate_seed(key):
    seed = 0
    for character in key:
        seed += ord(character)
    return seed

def initialize_frameOrderList(frameCount):
    frameOrderList = []
    for i in range(1, frameCount+1):
        frameOrderList.append(i)
    return frameOrderList

def shuffle_frameOrderList(seed, frameOrderList):
    random.seed(seed)
    random.shuffle(frameOrderList)
    return frameOrderList

def get_frameCount(frame_dir):
    frameCount = 0
    for path in pathlib.Path(frame_dir).iterdir():
        if path.is_file():
            frameCount += 1
    print("frameCount = ", frameCount)
    return frameCount


def bit_depth(image_type):
    if image_type == "L" or image_type == "P":
        return 1
    elif image_type == "RGB":
        return 3
    else:
        raise TypeError("Input type not supported")

def payload(input_message, input_bit, input_width, input_height):
        if len(input_message) > input_bit * input_width * input_height:
            return False
        return True

def encode(input_video, frame_dir, message, key, frameSequential=True, pixelSequential=True, encrypted=False, from_file=False, output_video="stego-generated.avi"):
    call(["ffmpeg", "-i", input_video, frame_dir+"/%d.png", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", input_video, "-q:a", "0", "-map", "a", "tempaudio/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    #fps = frame_extract(str(file_name), "temp")
    #change key to uppercase
    toUpperCase(key)
    if from_file:
        with open(message, "r") as f:
            message = f.read()
    if encrypted:
        message = classic.ExtendedVigenere.encrypt(message,key)
    #Initialize width and height for frame
    # frame = Image.open(str(frame_dir) + "/0.png")
    frame = Image.open(str(frame_dir) + "/1.png")
    width, height = frame.size
    print("width = ", width, " ,height = ", height)
    bit_depth = ImageSteganography.ImageSteganography.bit_depth(frame.mode)
    #calculate split_length
    #split_length = int((width*height)/bit_depth)-1
    split_length = int(width * height / bit_depth) - 1
    # split_length = 10
    print("split_length = ", split_length)
    #split_length = 2000000
    #initialize frameCount
    frameCount = get_frameCount(frame_dir)
    frameOrderList = initialize_frameOrderList(frameCount)
    #shuffle frameOrderList if not sequential
    if not frameSequential:
        print('not frameSequential')
        seed = calculate_seed(key)
        random.seed(seed)
        random.shuffle(frameOrderList)
        #frameOrderList = shuffle_frameOrderList(seed, frameOrderList)
        method_code = "4"
        # if not pixelSequential:
        #     method_code += "4"
    else:
        method_code = "3"
        # if not pixelSequential:
        #     method_code += "3"
        #insert to frame LSB
        #message = method_code + message
        #Split message into 255 string
        #print("split message into length = ", int((width*height)/bit_depth)-1)
        #messagepart_list =  splitString(message, int((width*height)/bit_depth)-1)
    if encrypted:
        method_code += "4"
    else:
        method_code += "3"
    #print('frameOrderList encode = ', frameOrderList)
    print("method_code encode = ", method_code)
    appendedList, frameZeroPassed = appendMethodCode(message, split_length, method_code, frameOrderList)
    if frameZeroPassed == True:
        appendedString = "".join(appendedList)
        messagepart_list = splitString(appendedString, split_length)
    else:
        messagepart_list = appendedList
    #print("appendedList = ", appendedList)
    #messagepart_list = splitString(appendedMessage, split_length)
    #messagepart_list =  splitString(message, int(2))
    #FOR TESTING PURPOSES
    #messagepart_list = []
    #messagepart_list.append(message)
    #print("messagepart_list = ", messagepart_list)
    #initialize message part index
    messagepart_index = 0
    #iterate for each message part
    for i in range(len(frameOrderList)):
        messagepart = ""
        if i < len(messagepart_list):
            messagepart = messagepart_list[i]
        messagepart_length = len(messagepart)
        #Open frame
        #frame = Image.open(str(frame_dir) +"/" + str(frameOrderList[messagepart_index]) + ".png")
        frameName = str(frame_dir) +"/" + str(frameOrderList[i]) + ".png"
        #print("frameName = ", frameName)
        #print()
        #Using lsb, insert message to frame
        ImageSteganography.ImageSteganography.hide_message(input_choice=method_code ,input_image=frameName, input_message=messagepart, input_key=key, output_image=frameName, pixelSequential=pixelSequential, from_file=False)
        #Save Image
        messagepart_index+=1
    #print("fps = ", fps)
    call(["ffmpeg", "-i", frame_dir+"/%d.png" , "-vcodec", "png", "tempmovie/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", "tempmovie/video.mov", "-i", "tempaudio/audio.mp3", "-codec", "copy", output_video, "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    #write_video(output_video=output_video, output_folder='data', fps = fps)

def image_psnr(input_image, output_image):
    print(input_image.size)
    width, height = input_image.size
    bit_depth = ImageSteganography.ImageSteganography.bit_depth(input_image.mode)
    
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
    if result == 0:
        psnr_value = 100
    else:
        psnr_value = 20 * math.log10(255 / result)

    print('PSNR:', psnr_value)
    if psnr_value >= 30:
        print('PSNR: good image quality')
    elif psnr_value < 30:
        print('PSNR: significant degraded image quality')
    return psnr_value

def video_psnr(input_video, input_dir, output_video, output_dir):
    call(["ffmpeg", "-i", input_video, input_dir+"/%d.png", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
    call(["ffmpeg", "-i", output_video, output_dir+"/%d.png", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

    print("sorted glob input = " ,sorted(glob.glob('./temp/*.png'),key=alphanum_key))
    input_img_array = []
    for filename in sorted(glob.glob('./'+input_dir+'/*.png'),key=alphanum_key):
        img = Image.open(filename)
        # height, width, layers = img.shape
        # size = (width,height)
        input_img_array.append(img)
    
    print("sorted glob output= " ,sorted(glob.glob('./temp/*.png'),key=alphanum_key))
    output_img_array = []
    for filename in sorted(glob.glob('./'+output_dir+'/*.png'),key=alphanum_key):
        img2 = Image.open(filename)
        # height2, width2, layers2 = img2.shape
        # size2 = (width2,height2)
        output_img_array.append(img2)

    total_psnr = 0
    for i in range(len(input_img_array)):
        print(input_img_array[i].size)
        print(output_img_array[i].size)
        total_psnr += image_psnr(input_img_array[i], output_img_array[i])
    psnr_value = total_psnr / len(input_img_array)

    print('VIDEO PSNR:', psnr_value)
    if psnr_value >= 30:
        print('VIDEO PSNR: good image quality')
    elif psnr_value < 30:
        print('VIDEO PSNR: significant degraded image quality')
    return psnr_value

if __name__ == "__main__":
    file_name = "3sec.avi"
    message = "a.txt"
    # try:
    #     open("data/" + file_name)
    # except IOError:
    #     print("-----------------------")
    #     print("(!) File not found ")
    #     exit()
    
    # extract frame
    #frame_extract(str(file_name), "temp")
    #call(["ffmpeg", "-i", "data/" + str(file_name), "temp/%d.png", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

    # extract audio
    #call(["ffmpeg", "-i", "data/" + str(file_name), "-q:a", "0", "-map", "a", "tempaudio/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

    ##encrypt and append string to frames
    #encode(input_video=file_name, frame_dir="temp", message=message, key="didik", frameSequential=False, pixelSequential=False, encrypted=True, from_file=True, output_video="stegomovie-3sec.mov")

    #write_video(output_video='stegomovie-3sec.avi', output_folder='data')

    # # #merge audio
    #call(["ffmpeg", "-i", "tempmovie/video.mov", "-i", "tempaudio/audio.mp3", "-codec", "copy", "data/stegomovie-3sec"+".mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

    #call(["ffmpeg", "-i", "data/stegomovie-3sec"+".mov", "temp2/%d.png", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

    # # #DECRYPT
    #file_name = "stegomovie-3sec.mov"

    # #extract frames
    #frame_extract(str(file_name), "temp2")

    # #decrypt
    #decodedMessage = decode(frame_dir="temp2",key="didik", input_video="data/stegomovie-3sec"+".mov")
    # decodedMessage = decode(frame_dir="temp2", input_video="stegomovie.mov", key="didik", output_message="decodedMessage.txt")
    # print("decodedMessageResult = ", decodedMessage)
    # print("end of message")

    #psnr
    #video_psnr(input_video="data/3sec.avi",input_dir="temp",output_video="stegomovie.mov",output_dir="temp2")