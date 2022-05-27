import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import numpy.random as ra
import scipy.signal as sig

# F=ma
# F=U
# F=-Lv
# ma = -LV + U
# a = -L/m

def main():
    n_steps = 500
    fs = 100
    n_vec = 2
    input = np.zeros(n_steps*fs)
    #SM variables (not CCF?)
    A_ana = np.array([[-0.8,-0.001],
                      [01.0,0]])
    A = A_ana*(1/fs) + np.identity(np.shape(A_ana)[0])
    B = np.array([[1],
                  [0]])
    H = np.array([[0],[1]])  #Different to normal: C is cov, H is state->observation

    C = 100
    Q = 0 #Filled out later

    s_act = np.zeros([n_steps*fs,n_vec, 1])  #Actual
    x = np.zeros([n_steps*fs,1])
    #KF variables
    s_pred = np.zeros([n_steps*fs,n_vec,n_vec]) #Predicted
    s_cor = np.zeros([n_steps*fs,n_vec,n_vec])  #Corrected
    K = np.zeros([n_steps*fs,n_vec,1])
    M_pred = np.zeros([n_steps*fs,n_vec,n_vec])
    M_cor = np.zeros([n_steps*fs,n_vec,n_vec])

    #Generate input
    for ss in range(100):
        idx = np.int64(np.round(ra.rand()*n_steps*fs-1)) + 1
        input[idx] = ra.randn()*2
    Q = input**2
    QQ = np.var(input)


    #Simulate
    for ss in range(n_steps*fs-1):
        if (ss != 0):
            s_act[ss] = A @ s_act[ss-1] + B*input[ss]
            #s_act[ss] = A @ s_act[ss-1] + B*ra.randn()*np.sqrt(QQ)
        x[ss] = H.T @ s_act[ss] + ra.randn()*np.sqrt(C)

    #Filter
    for ss in range(n_steps*fs-1):
        if (ss % n_steps == 0):
            print(ss/n_steps)
        if (ss != 0):
            s_pred[ss] = A @ s_cor[ss-1]
            M_pred[ss] = B @ B.T * Q[ss] + A @ M_cor[ss-1] @ A.T
            K[ss] = M_pred[ss] @ H /( H.T @ M_pred[ss] @ H + C)
            s_cor[ss] = s_pred[ss] + K[ss] @ (x[ss] - H.T @ s_pred[ss])
            M_cor[ss] = (np.identity(n_vec) - K[ss] @ H.T) @ M_pred[ss]
        else:
            s_cor[ss] = np.ones([n_vec,1])
            M_cor[ss] = np.identity(n_vec)

    plt.figure()
    plt.title("Simulation")
    plt.plot(x, label="x")
    plt.plot(s_act[:,1], label="s_act")
    plt.plot(s_act[:,0], label="d s_act/dt")
    plt.legend()

    plt.figure()
    plt.title("Filter")
    plt.plot(x, label="x")
    plt.plot(s_act[:,1], label="s_act")
    plt.plot(s_cor[:,1], label="s_cor")
    plt.plot(input, label="input")
    plt.plot(K[:,0], label="K_v")
    plt.plot(K[:,1], label="K_x")
    plt.legend()
    plt.show()

main()
