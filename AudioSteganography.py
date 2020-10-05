import classic
import wave
import random
from playsound import playsound

class AudioSteganography:
    @staticmethod
    def encode(filename_input, message, key, encrypt=False, filename_output="stegAudio.wav", method="sequential"):
        print("\nEncoding Starts..")
        audio = wave.open(filename_input, mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        message = classic.readFileBinary(message)
        if(encrypt):
            message = classic.ExtendedVigenere.encrypt(message, key)
        else:
            msg = ''
            for i in range(len(message)):
                msg = msg + chr(ord(message[i]))
            message = msg
        message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
        if(len(bits) > len(frame_bytes)-1):
            print("Message is too large to be hidden in desired audio file")
            return
        if(method == "sequential"):
            frame_bytes[0] = (frame_bytes[0] & 254) | 1
            for i, bit in enumerate(bits):
                frame_bytes[i+1] = (frame_bytes[i+1] & 254) | bit
        else:
            frame_bytes[0] = (frame_bytes[0] & 254) | 0
            seed = 0
            for i in range(len(key)):
                seed = seed + ord(key[i])
            random.seed(seed)
            for i, bit in enumerate(bits):
                num = random.randint(1, len(frame_bytes))
                frame_bytes[num] = (frame_bytes[num] & 254) | bit
        frame_modified = bytes(frame_bytes)
        newAudio =  wave.open(filename_output, 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        print(" |---->succesfully encoded inside " + filename_output)

    @staticmethod
    def decode(filename_steg, key, encrypted=False, extracted_message="extracted.txt"):
        print("\nDecoding Starts..")
        audio = wave.open(filename_steg, mode='rb')
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        code = frame_bytes[0] & 1
        if(code == 1):
            extracted = [frame_bytes[i] & 1 for i in range(1, len(frame_bytes))]
        else:
            seed = 0
            for i in range(len(key)):
                seed = seed + ord(key[i])
            random.seed(seed)
            extracted = []
            for i in range(1, len(frame_bytes)):
                num = random.randint(1, len(frame_bytes))
                extracted.append(frame_bytes[num] & 1)
            #extracted = [frame_bytes[random.randint(1, len(frame_bytes))] & 1 for i in range(1, len(frame_bytes))]
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        decoded = string.split("###")[0]
        if(encrypted):
            decoded = classic.ExtendedVigenere.decrypt(decoded, key)
        classic.writeFileBinary(extracted_message, decoded)
        print("Sucessfully decoded in "+extracted_message)
        audio.close()

def main():
    while(True):
        print("---Audio Steganography---")
        print("-------------------------")
        print("encode (format: encode filename_input message key encrypt? filename_output method (default encrypt?=False filename_output='stegAudio.wav' method='sequential/random'")
        print("decode (format: decode filename_steg key encrypted? filename_extracted (default encrypted?=False filename_extracted = 'extracted.txt'")
        print("play audio (format play filename)")
        print('-------------------------')
        command = input().split()
        print("-------------------------")
        if(command[0] == "encode" and (len(command) == 7 or len(command) >= 4)):
            if(len(command) == 7):
                AudioSteganography.encode(command[1], command[2], command[3], command[4], command[5], command[6])
            elif(len(command) == 6):
                AudioSteganography.encode(command[1], command[2], command[3], command[4], command[5])
            elif(len(command) == 5):
                AudioSteganography.encode(command[1], command[2], command[3], command[4])
            elif(len(command) == 4):
                AudioSteganography.encode(command[1], command[2], command[3], command[3])
            print()
        elif(command[0] == "decode" and (len(command) == 5 or len(command) == 4 or len(command) == 3)):
            if(len(command) == 5):
                AudioSteganography.decode(command[1], command[2], command[3])
            elif(len(command) == 4):
                AudioSteganography.decode(command[1], command[2], command[3])
            elif(len(command) == 3):
                AudioSteganography.decode(command[1], command[2])
            print()
        elif(command[0] == "play" and len(command) == 2):
            playsound(command[1])
        else:
            print("input incomplete")
            print()

'''filename_input = "sample.wav"
filename_output = "stegAudio.wav"
message = "sampleMessage.txt"
key = "king"
AudioSteganography.encode(filename_input, message, key)
AudioSteganography.decode(filename_output, key)'''
main()
