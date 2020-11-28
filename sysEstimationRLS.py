import numpy as np
import numpy.fft as nfft

import scipy.signal as sig
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt

import sysEstimationRLS_Test as test


def fetch_signal(filename):
    """
    Basically does nothing useful yet but swap the signal orders
    It might do more later.
    """

    rate, data = wav.read(filename)
    print(rate)
    return data, rate

def filter_arma(data, rate, verbose = False):
    """Filter using a preset ARMA system"""
    #Place poles by hand, it doesn't matter much. Values should be in hz
    #I can't be bothered playing with the radius.
    zeros = np.array([100, 2000, 4000])
    poles = np.array([200, 2000, 8000])
    z = 0.999 * np.exp(2j * np.pi * (zeros / (2 * rate)) )
    p = 0.999 * np.exp(2j * np.pi * (poles / (2 * rate)) )
    z = np.append(z, z.conj())
    p = np.append(p, p.conj())

    if (verbose):
        plt.figure()
        plt.title("Zero locations")
        plt.scatter(z.real, z.imag)
        print("Zero freqs as multiple of pi", np.angle(z)/np.pi)
        print("Zero mags", np.abs(z))
        plt.figure()
        plt.title("Pole locations")
        plt.scatter(p.real, p.imag)
        print("Pole freqs as multiple of pi", np.angle(p)/np.pi)
        print("Pole mags", np.abs(p))

    b, a = sig.zpk2tf(z, p, 1)
    output = sig.lfilter(b, a, data)
    if (verbose):
        h,w = sig.freqz(b, a, fs=rate)
        plt.figure()
        plt.title("test_function")
        plt.plot(h)
        plt.plot(w)
    return output

def throughRLS(R0,f0,rho,x_in,d_in,n_iter):
    """
    This is a stock implementation of an RLS algorithm
    Please check if faster algorithms are more applicable, I don't
        care about speed for this.

    I don't generate R0 because it means this algo can run on the
        same data multiple times.
    """

    #Initial checks and setup.
    if (len(d) != len(x)):
        print("WARNING:")
        print("Data vector length mismatch (non-fatal)")

    min_input_l = np.min([len(x),len(d)])
    filter_l = len(f0)

    if (n_iter < min_input_l):
        print("ERROR:")
        print("RLS doesn't have enough data for requested No iterations")

    R = np.zeros(np.shape(R0))
    R[:] = R0[:]
    f = np.zeros(filter_l)
    f[:] = f0[:]
    x = np.zeros(filter_l)
    y_out = np.zeros(min_input_l)
    e_out = np.zeros(min_input_l)

    for n in np.arange(0, min_input_l - 1):
        ### Work through this stage ###
        ###############################

        #update x vector
        x = np.roll(x,1)
        x[0] = x_in[n]
        #Do the "convolution", compute the error, save the result!
        y = np.sum(x * f)
        e = y - d[n]
        y_out[n] = y
        e_out[n] = e

        ### Prepare for the next stage ###
        ##################################
        k = np.matmul(R,x)
        f += k*e
        R = (1/rho)*(R - (np.outer(k,k))/(rho + np.inner(x,k)))

    return e_out, y_out


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


    raw_data, rate = fetch_signal(filename)
    filt_data = filter_arma(raw_data, rate)

    R0 = np.identity(n_taps)



main("test.wav")
