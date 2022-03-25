import numpy as np
import numpy.random as ra
import numpy.fft as nfft

import scipy.signal as sig
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt

import sysEstimationRLS as body


def check_arma(filename):
    """
    Generic test function for the ARMA
    """
    raw_data, rate, n_samples, t_data = body.fetch_signal(filename)
    print(rate)
    filt_data = body.filter_arma(raw_data, rate, True)
    raw_fft = 10*np.log10(np.abs(nfft.fft(raw_data)))
    filt_fft = 10*np.log10(np.abs(nfft.fft(filt_data)))
    print(raw_data)
    print(filt_data)
    plt.figure()
    plt.plot(raw_data, label="raw")
    plt.plot(filt_data, label="filtered")
    plt.figure()
    plt.figure()
    freqs = np.linspace(0, rate, len(raw_data))
    plt.plot(freqs, raw_fft, label="raw")
    plt.plot(freqs, filt_fft, label="filt")
    plt.plot(freqs, filt_fft - raw_fft, label="change")
    plt.legend()
    plt.show()

def main(filename):
    """
    #Plan
    ##################
    #Get a test signal (DONE)
    #Generate some kind of system (ARMA)
    #Implement an RLS for system estimation
    #See how well I can estimate it!
    """

    n_taps = 32
    delta = 1e-5   #This is a mostly noiseless process, but we need reasonable convergence
    rho = 0.999     #This is a stationary process, but set this to ~0.999 for stability!

    raw_data, rate, n_samples, t_data = body.fetch_signal(filename)

    in_data = np.zeros(n_samples)
    #Add random noise powers, magic numbers, but I can't be bothered
    in_data[:] = raw_data[:] + 0.2*ra.randn(n_samples)
    filt_data = body.filter_arma(in_data, rate) + 1*ra.randn(n_samples)

    R0 = np.identity(n_taps)*delta
    f0 = np.zeros(n_taps)

    e, y = body.throughRLS(R0,f0,rho,in_data,filt_data,n_samples,False)

    plt.figure()
    plt.plot(e)
    plt.title("Approximation error")


    plt.figure()
    plt.plot(in_data, label = "raw audio")
    plt.plot(filt_data, label = "arma filtered audio")
    plt.plot(y, label = "Model filtered audio")
    plt.legend()
    plt.title("Values of signals")

    plt.show()


main("test.wav")
