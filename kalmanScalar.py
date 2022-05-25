import matplotlib.pyplot as plt
import numpy as np
import numpy.random as ra
import scipy.signal as sig

# Kalman filtering equations from Kay
#
#
#
#
#

def main():
    n_steps = 500;
    input = np.zeros(n_steps)
    #SM variables
    A = 0.95
    C = 1e-1
    Q = 0 #Filled out later

    s_act = np.zeros(n_steps)  #Actual
    x = np.zeros(n_steps)
    #KF variables
    s_pred = np.zeros(n_steps) #Predicted
    s_cor = np.zeros(n_steps)  #Corrected
    K = np.zeros(n_steps)
    M_pred = np.zeros(n_steps)
    M_cor = np.zeros(n_steps)


    #Generate input
    for ss in range(10):
        idx = np.int64(np.round(ra.rand()*n_steps-1)) + 1
        input[idx] = 1
    Q = input**2
    QQ = np.var(input)
    #simulate
    for ss in range(n_steps-1):
        if (ss != 0):
            s_act[ss] = A * s_act[ss-1] + input[ss]
            #s_act[ss] = A * s_act[ss-1] + ra.randn()*np.sqrt(Q)
        x[ss] = s_act[ss] + ra.randn()*np.sqrt(C)

    #Filter stage
    for ss in range(n_steps-1):
        if (ss != 0):
            s_pred[ss] = A * s_cor[ss-1]
            M_pred[ss] = QQ + A*A*M_cor[ss-1]

            K[ss] = M_pred[ss] /( M_pred[ss] + C)
            s_cor[ss] = s_pred[ss] + K[ss]*(x[ss] - s_pred[ss])
            M_cor[ss] = (1-K[ss])*M_pred[ss]
        else:
            s_cor[ss] = 0
            M_cor[ss] = C

    plt.figure()
    plt.plot(s_act, label="s_act")
    plt.plot(x, label="x")
    plt.plot(s_cor, label="s_cor")

    plt.figure()
    plt.plot(x, label="x")
    plt.plot(s_pred, label="s_pred-1")
    plt.plot(M_pred, label="M_pred-2")
    plt.plot(K, label="K-3")
    plt.plot(s_cor, label="s_cor-4")
    plt.plot(M_cor, label="M_cor-5")
    plt.plot(s_act, label="s_act")
    plt.legend()
    plt.show()


main()
