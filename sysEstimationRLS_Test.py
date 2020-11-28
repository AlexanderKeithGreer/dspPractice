import numpy as np
import numpy.fft as nfft

import scipy.signal as sig
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt

import sysEstimationRLS as body


def check_arma(filename):
    """
    Generic test function for the ARMA
    """
    raw_data, rate = body.fetch_signal(filename)
    print(rate)
    filt_data = body.filter_arma(raw_data, rate, True)
    raw_fft = 10*np.log10(np.abs(nfft.fft(raw_data)))
    filt_fft = 10*np.log10(np.abs(nfft.fft(filt_data)))
    print(raw_data)
    print(filt_data)
    plt.figure()
    freqs = np.linspace(0, rate, len(raw_data))
    plt.plot(freqs, raw_fft, label="raw")
    plt.plot(freqs, filt_fft, label="filt")
    plt.plot(freqs, filt_fft - raw_fft, label="change")
    plt.legend()
    plt.show()
