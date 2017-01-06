#!/usr/bin/python3

import numpy as np

from scipy.signal import blackmanharris, fftconvolve
from numpy import argmax, mean, diff, log
from matplotlib.mlab import find
from parabolic import parabolic
from scipy.signal import fftconvolve, kaiser, decimate
from numpy.fft import rfft

# from: https://github.com/endolith/waveform-analyzer
def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = diff(corr)
    start = find(d > 0)[0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
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


def format_sig(data, channels, method = 'first'):
    new_sig = []
    try:
        sig = np.frombuffer(data, dtype='int16').reshape(-1, channels)
        for val in sig[:,0]:
            new_val = val / 2**15
            if abs(new_val) >= 0.0:
                new_sig.append(new_val)
    except:
        new_sig = []
        print("ERROR")
    return new_sig