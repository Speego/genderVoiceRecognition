#!/usr/bin/python3

import os
import sys

if __name__ == '__main__':
    folder = sys.argv[1]
    for wav_file in os.listdir(folder):
        print(wav_file)
        file = folder + '/' + wav_file
        os.system('python sygnaly3.py ' + file)
        print('-----')
