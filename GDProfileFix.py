# -*- coding: utf-8 -*-

import base64
import os
import shutil
import struct
import time
import zlib

saves = ['CCGameManager.dat', 'CCLocalLevels.dat']

if __name__ == '__main__':
    os.chdir(os.getenv('localappdata') + '\\GeometryDash\\')

    print('Geometry Dash Profile Fix v0.1 by WEGFan')
    print()
    print('This tool can fix most problems caused unable to open the game by the save files.')
    print('(double clicking the game won\'t bring up any window, but moving the save files to other folders can open the game)')
    print('If you encounter any problem (unable to fix / doesn\'t work after fixed), feel free to create an issue.')
    print('Save files location:' + os.getcwd())
    print()

    # backup original file
    bakFolder = f'backup-{int(time.time())}'
    os.mkdir(bakFolder)
    for saveFile in saves:
        try:
            shutil.copyfile(saveFile, bakFolder + '\\' + saveFile)
        except:
            pass
    print('Save files backed up to ' + os.getcwd() + '\\' + bakFolder)
    print()

    input('Press Enter to fix...')
    print()

    for saveFile in saves:
        try:
            with open(saveFile, 'rb') as f:
                saveData = f.read()

            # decrypt
            decrypted = []
            for i in saveData:
                decrypted.append(i ^ 11)

            decryptedString = bytearray(decrypted).decode().replace('-', '+').replace('_', '/')
            decodedByteArray = base64.b64decode(decryptedString.encode())
            finString = zlib.decompress(decodedByteArray[10:], -zlib.MAX_WBITS).decode()

            # fix (i don't know why simply add spaces works...)
            fixed = finString.replace('><', '> <', 50)

            # encrypt
            fixedByteArray = fixed.encode()

            compressedData = zlib.compress(fixedByteArray)
            crc32 = struct.pack('I', zlib.crc32(fixedByteArray))
            dataSize = struct.pack('I', len(fixedByteArray))

            compressed = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x0b' + compressedData[2:-4] + crc32 + dataSize
            encodedByteArray = base64.b64encode(compressed).decode().replace('+', '-').replace('/', '_').encode()

            encrypted = []
            for i in encodedByteArray:
                encrypted.append(i ^ 11)
            result = bytearray(encrypted)

            with open(saveFile, 'wb') as f:
                f.write(result)
        except FileNotFoundError:
            print('Can\'t find ' + saveFile + '!')
        except:
            print('There was an issue fixing ' + saveFile + '!')
    print()
    input('Done! Press Enter to exit...')
