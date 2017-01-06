#!/usr/bin/python3

import wave
import sys

from numpy import argmax, mean, diff, percentile, frombuffer
from matplotlib.mlab import find
from scipy.signal import fftconvolve

def parabolic(f, x):
    try:
        xv = 1/2. * (f[x-1] - f[x+1]) / (f[x-1] - 2 * f[x] + f[x+1]) + x
        yv = f[x] - 1/4. * (f[x-1] - f[x+1]) * (xv - x)
    except:
        return (0,0)
    return (xv, yv)

# from: https://github.com/endolith/waveform-analyzer
def freq_from_autocorr(sig, fs):
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[(int)(len(corr)/2):]

    d = diff(corr)
    greaterThanZero = (find(d > 0))

    if len(greaterThanZero) == 0:
        return 1000
    else :
        start = greaterThanZero[0]
        peak = argmax(corr[start:]) + start
        px, py = parabolic(corr, peak)

        return fs / px

def voice_from_signal(signal, srate, step = 512, width = 4096, low = 50, high = 280):
    voice = []
    start = 0
    end = len(signal)
    while start < end - width:
        hertz_freq = freq_from_autocorr(signal[start:(start + width)], srate)
        abs_sig = []

        if hertz_freq > low and hertz_freq < high:
            voice = voice + [hertz_freq]
        start += step
    return voice

def format_sig(data, channels):
    new_sig = []
    try:
        sig = frombuffer(data, dtype='int16').reshape(-1, channels)
        for val in sig[:,0]:
            new_val = val / 2**15
            if abs(new_val) >= 0.0:
                new_sig.append(new_val)
    except:
        new_sig = []
    return new_sig

def check_voice(sig, framerate, low = 35, high = 280, width = 16384, step = 8192):
    tab = voice_from_signal(sig, framerate, low = low, high = high, width = width, step = step)
    avr = mean(tab)
    q25 = percentile(tab, 25)
    q75 = percentile(tab, 75)
    iqr = q75 - q25

    return (avr, iqr)

def decisionTree(avr, iqr):
    if avr >= 170:
        gender = 'K'
    elif iqr >= 135:
        gender = 'K'
    else:
        gender = 'M'

    return gender

if __name__ == '__main__':
    wav_file = sys.argv[1];
    w = wave.open(wav_file)
    framerate = w.getframerate()
    frames = w.getnframes()
    channels = w.getnchannels()
    width = w.getsampwidth()
    data = w.readframes(frames)
    sig = format_sig(data, channels)
    iqr = 0
    try:
        avr,iqr = check_voice(sig, framerate, low = 35, high = 280, width = 16384, step = 8192)
    except:
        try:
            avr,iqr = check_voice(sig, framerate, low = 35, high = 280, width = 2048, step = 2048)
        except:
            avr = 200 # woman

    gender = decisionTree(avr, iqr)
    print(gender)
