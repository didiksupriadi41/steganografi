import string
import random
from math import ceil
import numpy as np
ALPHABET = string.ascii_uppercase

def readFileText(file):
    f=open(file, mode='r')
    message=''
    for ch in f.read():
        if 65 <= ord(ch) <= 90 or 97 <= ord(ch) <= 122:
            message+=ch.upper()
    f.close()
    return message

def writeFileText(file, message):
    f=open(file, mode='w')
    for ch in message:
        f.write(ch)
    f.close()

def readFileBinary(file):
    message = []
    with open(file, "rb") as f:
        byte = f.read(1)
        while byte:
            message.append(byte)
            byte = f.read(1)
    return message

def writeFileBinary(file, message):
    f = open(file, "wb")
    for byte in message:
        f.write(byte.encode())
    f.close()

def groupMessagePerFiveCharacter(message):
    return ' '.join(message[i:i+5] for i in range(0,len(message),5))

#Build shifted alphabet
def offset(char, offset):
    return ALPHABET[(ALPHABET.index(char)+offset)%26]

class Vigenere:
    @staticmethod
    def encrypt(message, key):
        for char in message:
            if(char.isalpha() == False):
                return "TEXT CAN ONLY CONTAIN ALPHABET"
        return ''.join(map(offset, message, list(map(lambda x: ALPHABET.index(x), key))*(len(message)//len(key)+1)))

    @staticmethod
    def decrypt(ciphertext, key):
        for char in ciphertext:
            if(char.isalpha() == False):
                return "TEXT CAN ONLY CONTAIN ALPHABET"
        return ''.join(map(offset, ciphertext, list(map(lambda x: 26-ALPHABET.index(x), key))*(len(ciphertext)//len(key)+1)))

class AutoKeyVigenere:
    @staticmethod
    def encrypt(message, key):
        return Vigenere.encrypt(message, AutoKeyVigenere.lengthenKey(message, key))
    
    @staticmethod
    def decrypt(message, key):
        return Vigenere.decrypt(message, key)

    @staticmethod
    def lengthenKey(message, key):
        if(len(key) < len(message)):
            for i in range(len(message)-len(key)):
                key = key + message[i]
        return key

class FullVigenere:
    @staticmethod
    def makeTable():
        table = []
        for i in range(len(ALPHABET)):
            l = list.copy(list(ALPHABET))
            random.shuffle(l)
            table.append(l)
        return table

    @staticmethod
    def encrypt(message, key, table):
        ciphertext = ''
        j = 0
        for char in message:
            ciphertext = ciphertext + table[ord(key[j])-65][ord(char)-65]
            if(j < len(key)-1):
                j = j + 1
            else:
                j = 0
        return ciphertext

    @staticmethod
    def decrypt(message, key, table):
        plaintext = ''
        j = 0
        keyM = ''
        for i in range(len(message)):
            keyM = keyM + key[i % len(key)]
        for char in keyM:
            for i in range(26):
                if(ord(table[ord(char)-65][i])-65 == ord(message[j])-65):
                    plaintext = plaintext + chr(i+65)
                    break
            j = j + 1
        return plaintext

class ExtendedVigenere:
    @staticmethod
    def generateKey(message, key):
        keyM = ''
        for i in range(len(message)):
            keyM = keyM + key[i % len(key)]
        return keyM

    @staticmethod
    def encrypt(message, key):
        ciphertext = ''
        key = ExtendedVigenere.generateKey(message, key)
        for i in range(len(message)):
            ciphertext = ciphertext + chr((ord(message[i]) + ord(key[i % len(key)])) % 256)
        return ciphertext

    @staticmethod
    def decrypt(message, key):
        plaintext = ''
        for i in range(len(message)):
            plaintext = plaintext + chr((ord(message[i]) - ord(key[i % len(key)])) % 256)
        return plaintext

class Affine:
    @staticmethod
    def modReverse(a, b):
        r, s, t = [min(a, b), max(a, b)], [1, 0], [0,1]
        while r[-1]!=1:
            q = r[-2]//r[-1]
            r.append(r[-2]-q*r[-1])
            s.append(s[-2]-q*s[-1])
            t.append(t[-2]-q*t[-1])
        return (s[-1]%r[1])

    #key should be the tuple
    @staticmethod
    def encrypt(message, key):
        return ''.join(ALPHABET[(ALPHABET.index(ch)*key[0]+key[1])%26] for ch in message)

    #key should be the tuple
    @staticmethod
    def decrypt(ciphertext, key):
        try:
            return ''.join(ALPHABET[Affine.modReverse(key[0], 26)*(ALPHABET.index(ch)-key[1])%26] for ch in ciphertext)
        except ZeroDivisionError:
            pass

class SuperEncryption:
    @staticmethod
    def encrypt(message, key_vigenere, key_transposition):
        ciphertext = Vigenere.encrypt(message, key_vigenere)
        modr = (len(ciphertext) % key_transposition)
        if(modr != 0):
            for i in range(abs(modr-key_transposition)):
                ciphertext = ciphertext + 'X'
        splt = [ciphertext[i:i+key_transposition] for i in range(0, len(ciphertext), key_transposition)]
        ciphertext = ''
        for i in range(key_transposition):
            for j in range(len(splt)):
                ciphertext = ciphertext + splt[j][i]
        return ciphertext

    @staticmethod
    def decrypt(ciphertext, key_vigenere, key_transposition):
        n = ceil(len(ciphertext)/key_transposition)
        modr = (len(ciphertext) % n)
        if(modr != 0):
            for i in range(abs(modr-n)):
                ciphertext = ciphertext + 'X'
        splt = [ciphertext[i:i+n] for i in range(0, len(ciphertext), n)]
        ciphertext = ''
        for i in range(n):
            for j in range(key_transposition):
                ciphertext = ciphertext + splt[j][i]
        return Vigenere.decrypt(ciphertext, key_vigenere)


class Playfair:
    @staticmethod
    def buildtable(key):
        return ''.join(sorted(set(key), key=lambda x: key.index(x)))+''.join([ch for ch in ALPHABET if not (ch in key) and ch!='J'])

    #Padding message with X if two letters found in message in a row or length of message is odd
    @staticmethod
    def padding(message):
        list_message=list(message)
        i = 1
        while i < len(list_message):
            if list_message[i]==list_message[i-1]:
                list_message.insert(i, 'X')
            i += 2
        if len(list_message)%2!=0:
            list_message.append('X')
        return [''.join(list_message[a:a+2]) for a in range(0, len(list_message), 2)]

    @staticmethod
    def substitution(message, table, *, mode):
        #table=Playfair.buildtable(key)
        if mode == 1:
            message=message.replace('J', 'I')
        list_message=Playfair.padding(message)
        list_pos=[[[table.index(elem[0])//5, table.index(elem[0])%5], [table.index(elem[1])//5, table.index(elem[1])%5]] for elem in list_message]
        list_pos2=[]
        for elem in list_pos:
            if elem[0][0]==elem[1][0]:
                list_pos2.append([[elem[0][0], (elem[0][1]+mode)%5], [elem[1][0], (elem[1][1]+mode)%5]])
            elif elem[0][1]==elem[1][1]:
                list_pos2.append([[(elem[0][0]+mode)%5, elem[0][1]], [(elem[1][0]+mode)%5, elem[1][1]]])
            else:
                list_pos2.append([[elem[0][0], elem[1][1]], [elem[1][0], elem[0][1]]])
        c=''.join([table[e[0][0]*5+e[0][1]]+table[e[1][0]*5+e[1][1]] for e in list_pos2])
        return c

    @staticmethod
    def encrypt(message, key):
        for char in message:
            if(char.isalpha() == False):
                return "TEXT CAN ONLY CONTAIN ALPHABET"
        return Playfair.substitution(message, key, mode=1)

    @staticmethod
    def decrypt(message, key):
        for char in message:
            if(char.isalpha() == False):
                return "TEXT CAN ONLY CONTAIN ALPHABET"
        return Playfair.substitution(message, key, mode=-1)

class Hill:
    @staticmethod
    def generateMatrix():
        #return np.matrix([[17, 17, 5], [21, 18, 21], [2, 2, 19]])
        return np.matrix([[random.randrange(1, 100, 1), random.randrange(1, 100, 1), random.randrange(1, 100, 1)], [random.randrange(1, 100, 1), random.randrange(1, 100, 1), random.randrange(1, 100, 1)], [random.randrange(1, 100, 1), random.randrange(1, 100, 1), random.randrange(1, 100, 1)]])

    @staticmethod
    def encrypt(message, key):
        ciphertext = ''
        while (len(message) % 3 != 0):
            message = message + 'X'
        i = 0
        while(i < len(message)):
            a = np.matrix([[ord(message[i])-65], [ord(message[i+1])-65], [ord(message[i+2])-65]])
            b = key.dot(a) % 26
            ciphertext = ciphertext + chr(b.item(0) + 65)
            ciphertext = ciphertext + chr(b.item(1) + 65)
            ciphertext = ciphertext + chr(b.item(2) + 65)
            i = i + 3
        return ciphertext

    @staticmethod
    def decrypt(message, key):
        plaintext = ''
        while (len(message) % 3 != 0):
            message = message + 'X'
        i = 0
        while(i < len(message)):
            a = np.matrix([[ord(message[i])-65], [ord(message[i+1])-65], [ord(message[i+2])-65]])
            m = Hill.modinv(np.linalg.det(key), 26)
            b = m*key.getH().dot(a) % 26
            plaintext = plaintext + chr(b.item(0) + 65)
            plaintext = plaintext + chr(b.item(1) + 65)
            plaintext = plaintext + chr(b.item(2) + 65)
            i = i + 3
        return plaintext
    
    @staticmethod
    def iterative_egcd(a, b):
        x,y, u,v = 0,1, 1,0
        while a != 0:
            q,r = b//a,b%a; m,n = x-u*q,y-v*q # use x//y for floor "floor division"
            b,a, x,y, u,v = a,r, u,v, m,n
        return b, x, y

    @staticmethod
    def modinv(a, m):
        g, x, y = Hill.iterative_egcd(a, m) 
        if g != 1:
            return None
        else:
            return x % m



"""if __name__=='__main__':
    #Vigenere test
    print('---Vigenere---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = Vigenere.encrypt(test, 'FORTIFICATION'.upper())
    d = Vigenere.decrypt(c, 'FORTIFICATION'.upper())
    print(c)
    print(d)

    #Affine test
    print('---Affine---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = Affine.encrypt(test, (5, 7))
    print(c)
    d = Affine.decrypt(c, (5, 7))
    print(d)

    #Playfair test
    print('---Playfair Cipher---')
    key=Playfair.buildtable('monarchy'.upper())
    c = Playfair.encrypt('wearediscoveredsaveyourselfx'.upper(), key)
    print(c)
    d = Playfair.decrypt(c, key)
    print(d)

    #Super Encryption test
    print('---Super Encryption---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = SuperEncryption.encrypt(test, 'FORTIFICATION'.upper(), 6)
    d = SuperEncryption.decrypt(c, 'FORTIFICATION'.upper(), 6)
    print(c)
    print(d)

    #Auto Vigenere test
    print('---Auto Vigenere---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = AutoKeyVigenere.encrypt(test, 'FORTIFICATION'.upper())
    d = AutoKeyVigenere.decrypt(c, 'FORTIFICATION'.upper())
    print(c)
    print(d)
    
    #Full Vigenere test
    print('---Full Vigenere---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    table = FullVigenere.makeTable()
    c = FullVigenere.encrypt(test, 'FORTIFICATION'.upper(), table)
    d = FullVigenere.decrypt(c, 'FORTIFICATION'.upper(), table)
    print(c)
    print(d)

    #Extended Vigenere test
    print('---Extended Vigenere---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    c = ExtendedVigenere.encrypt(test, 'FORTIFICATION'.upper())
    d = ExtendedVigenere.decrypt(c, 'FORTIFICATION'.upper())
    print(c)
    print(d)

    #Extended Vigenere test
    print('---Extended Vigenere---')
    test = 'DEFENDTHEEASTWALLOFTHECASTLE'
    fin = readFileBinary('pakWindy.jpg')
    c = ExtendedVigenere.encrypt(fin, 'FORTIFICATION'.upper())
    writeFileBinary('tes', c)
    d = ExtendedVigenere.decrypt(c, 'FORTIFICATION'.upper())
    writeFileBinary('te.jpg', d)

    #Hill test
    print('---Hill Vigenere---')
    test = 'PAYMOREMONEY'
    key = Hill.generateMatrix()
    c = Hill.encrypt(test, key)
    d = Hill.decrypt(c, key)
    print(c)
    print(d)"""