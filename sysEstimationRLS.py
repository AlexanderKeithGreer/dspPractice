import numpy as np
import numpy.fft as nfft
import numpy.linalg as la
import numpy.random as ra

import scipy.signal as sig
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt


def fetch_signal(filename):
    """
    Basically does nothing useful yet but swap the signal orders
    It might do more later.
    """

    fs, data = wav.read(filename)
    n_samples = len(data)
    t_data = n_samples/fs
    return data, fs, n_samples, t_data

def filter_arma(data, rate, verbose = False):
    """Filter using a preset ARMA system"""
    #Place poles by hand, it doesn't matter much. Values should be in hz
    #I can't be bothered playing with the radius.
    zeros = np.array([100, 2000, 400, 412, 2500, 3500,  4000])
    poles = np.array([200, 2000, 3000, 8000])
    z = 0.99 * np.exp(2j * np.pi * (zeros / (2 * rate)) )
    p = 0.99 * np.exp(2j * np.pi * (poles / (2 * rate)) )
    #Make the filter use real transfer function values!
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

def throughRLS(R0,f0,rho,x_in,d_in,n_iter,verbose=False):
    """
    This is a stock implementation of an RLS algorithm
    Please check if faster algorithms are more applicable, I don't
        care about speed for this.

    I don't generate R0 because it means this algo can run on the
        same data multiple times.
    """

    #Initial checks and setup.
    if (len(d_in) != len(x_in)):
        print("WARNING:")
        print("Data vector length mismatch (non-fatal)")

    l_min_input = np.min([len(x_in),len(d_in)])
    l_filter = len(f0)

    if (n_iter > l_min_input):
        print("ERROR:")
        print("RLS doesn't have enough data for requested No iterations")

    if (np.max(np.shape(R0)) != l_filter):
        print("ERROR:")
        print("R^-1 doesn't match the filter length")

    R = np.zeros(np.shape(R0))
    R[:] = R0[:]
    f = np.zeros(l_filter)
    f[:] = f0[:]
    x = np.zeros(l_filter)
    y_out = np.zeros(l_min_input)
    e_out = np.zeros(l_min_input)

    #Start filter
    for n in np.arange(0, n_iter - 1):
        ### Work through the current stage ###
        ###############################

        #update x vector
        x = np.roll(x,1)
        x[0] = x_in[n]
        if (verbose):
            print("\nx = ", x)
            print("x_in,d_in = ", x_in[n], " , ", d_in[n])

        #Do the "convolution", compute the error, save the result!
        y = np.sum(x * f)
        if (verbose):
            print("y = ", y)
        e = d_in[n] - y
        if (verbose):
            print("e = ", e)
        y_out[n] = y
        e_out[n] = e

        ########## Prepare for the next stage #######
        ### These value affect the next iteration ###
        #############################################
        k = np.matmul(R,x)
        if (verbose):
            print("k = ", k)
        f = f + k*e
        if (verbose):
            print("f = ", f)

        R = (1/rho)*(R - (np.outer(k,k))/(rho + np.inner(x,k)))
        if (verbose):
            print("R = \n", la.inv(R))

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

    n_taps = 128
    delta = 1e-5   #This is a mostly noiseless process, but we need reasonable convergence
    rho = 0.999     #This is a stationary process, but set this to ~0.999 for stability!

    raw_data, rate, n_samples, t_data = fetch_signal(filename)
    in_data = np.zeros(n_samples)
    #Add random noise powers, magic numbers, but I can't be bothered
    in_data[:] = raw_data[:] + 0.2*ra.randn(n_samples)
    filt_data = filter_arma(in_data, rate) + 1*ra.randn(n_samples)

    R0 = np.identity(n_taps)*delta
    f0 = np.zeros(n_taps)

    e, y = throughRLS(R0,f0,rho,in_data,filt_data,n_samples,False)

    plt.figure()
    plt.plot(e)
    plt.title("Approximation error")


    plt.figure()
    plt.plot(in_data, label = "raw audio")
    plt.plot(filt_data, label = "arma filtered audio")
    plt.plot(y, label = "Model filtered audio")
    plt.legend()
    plt.title(Values of signals)

    plt.show()


main("test.wav")
