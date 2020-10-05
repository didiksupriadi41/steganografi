import classic
import wave
import random
from playsound import playsound

class AudioSteganography:
    @staticmethod
    def encode(filename_input, message, key, filename_output="stegAudio.wav", method="random"):
        
        print("\nEncoding Starts..")
        audio = wave.open(filename_input, mode="rb")
        frame_bytes = bytearray(list(audio.readframes(audio.getnframes())))
        message = classic.readFileBinary(message)
        message = classic.ExtendedVigenere.encrypt(message, key)
        message = message + int((len(frame_bytes)-(len(message)*8*8))/8) *'#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message])))
        if(len(bits) > len(frame_bytes)-1):
            print("Message too large to be hidden in desired audio file")
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
                if(i < 10):
                    print(num)
                    print(frame_bytes[num])
        frame_modified = bytes(frame_bytes)
        newAudio =  wave.open(filename_output, 'wb')
        newAudio.setparams(audio.getparams())
        newAudio.writeframes(frame_modified)

        newAudio.close()
        audio.close()
        print(" |---->succesfully encoded inside " + filename_output)

    @staticmethod
    def decode(filename_steg, key, extracted_message="extracted.txt"):
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
                if(i < 10):
                    print(num)
                    print(frame_bytes[num])
            #extracted = [frame_bytes[random.randint(1, len(frame_bytes))] & 1 for i in range(1, len(frame_bytes))]
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        decoded = string.split("###")[0]
        decoded = classic.ExtendedVigenere.decrypt(decoded, key)
        classic.writeFileBinary(extracted_message, decoded)
        print("Sucessfully decoded in "+extracted_message)
        audio.close()

def main():
    while(True):
        print("---Audio Steganography---")
        print("encode (format: encode filename_input message key filename_output method (default filename_output = 'stegAudio.wav' method='sequential/random'")
        print("decode (format: decode filename_steg key filename_extracted (default filename_extracted = 'extracted.txt'")
        print("play audio (format play filename")
        command = input()
        command.split()
        if(command[0] == "encode" and len(command == 6)):
            AudioSteganography.encode(command[1], command[2], command[3], command[4], command[5])
        elif(command[1] == decode and len(command) == 4):
            AudioSteganography.decode(command[1], command[2], command[3])
        elif(command[1] == "play" and len(command) == 2):
            playsound(command[1])
        else:
            print("input incomplete")

filename_input = "sample.wav"
filename_output = "sampleSteg.wav"
message = "sampleMessage.txt"
key = "king"
AudioSteganography.encode(filename_input, message, key)
AudioSteganography.decode(filename_output, key)
playsound("sample.wav")
