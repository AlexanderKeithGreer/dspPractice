import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy.random as ra

def basic_PCA_example():
    #Generate signals; use a moving average to concentrate energy at the
    #  lower frequencies
    T = 1000
    s = np.zeros((2,T))
    s[0,:] = np.convolve(1*ra.randn(T), np.ones(25), mode="same")
    s[1,:] = np.convolve(1*ra.randn(T), np.ones(25), mode="same")

    #Spread the perfect signals over the channels and add noise
    A = np.array([[-1, -1],[-1,1],[1,-1],[-1, -1]])
    x = np.matmul(A, s)
    x += 15*ra.randn(np.shape(x)[0],np.shape(x)[1])

    #Plot perfect signals
    plt.figure()
    plt.plot(s[0,:],label="s1")
    plt.plot(s[1,:],label="s2")
    plt.legend()

    #Plot sensor received signals
    plt.figure()
    plt.plot(x[0,:],label="x1")
    plt.plot(x[1,:],label="x2")
    plt.plot(x[2,:],label="x3")
    plt.plot(x[3,:],label="x4")
    plt.legend()

    #Actually use the PCA
    Cxx = np.inner(x,x)/max(x.shape)
    print(np.shape(Cxx))
    val, vec = la.eig(Cxx)
    print("Eigenvalues:\n", val)
    print("Eigenvectors:\n", vec)
    y0 = np.inner(vec[:,0], x.T).flatten()
    y1 = np.inner(vec[:,1], x.T).flatten()

    #Plot results
    plt.figure()
    plt.plot(s[1,:]/max(s[1,:]),label="s2")
    plt.plot(y0/max(y0),label="y2")
    plt.legend()

    plt.figure()
    plt.plot(s[0,:]/max(s[0,:]),label="s1")
    plt.plot(y1/max(y1),label="y1")
    plt.legend()

    plt.show()


example_given()
