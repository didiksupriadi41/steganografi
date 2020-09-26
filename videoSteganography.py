import classic

class videoSteganography:
    @staticmethod
    def merge(self, message, video, key='', encrypt=False):
        if encrypt:
            message = classic.ExtendedVigenere.encrypt(message, key)
    
    pass

if __name__=='__main__':
    pass