#!/usr/bin/python3
import numpy as np


def voice_from_signal(signal, srate, step = 512, width = 4096, low = 50, high =280):
    voice = []
    start = 0
    end = len(signal)
    while start < end - width:
        spectrum = np.fft.fft(signal[start:(start + width)])
        freqs = np.fft.fftfreq(len(spectrum))
        peak = np.argmax(np.abs(spectrum))
        freq = freqs[peak]
        hertz_freq = abs(freq * srate)
        if hertz_freq > low and hertz_freq < high:
            voice = voice + [hertz_freq]
        start += step
    return voice


def format_sig(data, channels, method = 'first'):
    new_sig = []
    try:
        sig = np.frombuffer(data, dtype='int16').reshape(-1, channels)
        for val in sig[:,0]:
            new_sig.append(val / 2**15)
    except:
        new_sig = []
        print("ERROR")
    return new_sig
