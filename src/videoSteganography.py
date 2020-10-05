import classic
from PIL import image
import shutil, cv2, os

def split2len(s, n):
    def _f(s, n):
        while s:
            yield s[:n]
            s = s[n:]
    return list(_f(s, n))

class videoSteganography:
    @staticmethod
    def merge(self, message, video, key='', encrypt=False):
        if encrypt:
            message = classic.ExtendedVigenere.encrypt(message, key)
        message_split_255 = split2len(message, 255)
        for message in message_255:
            message_length = len(message)

        pass
    
    @staticmethod
    def unmerge(self, message, video, key='', decrypt=False):
        if decrypt:
            message = classic.ExtendedVigenere.decrypt(message, key)
        pass


if __name__=='__main__':
    pass