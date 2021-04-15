import numpy as np
import numpy.fft as nfft
import scipy.signal as sig
import matplotlib.pyplot as plt

def bnlms (ref, surv, mu, gamma, block_size, past_coef):
    """ Implements the fast (FFT!) block NLMS algorithm described in
            Adaptive Filters - Theory and Applications
            2nd Ed
            Behrouz Farhang-Boroujeny
            Ch 8 ("Block Implementation of Adaptive Filters")

        The block diagram on page 261 should illustrate the processes described
            in the comments I've left

        Let L=N, at least for now

    And then the world will know
        and then the world will see
        and that world shall cease to be
    """
    ref_l = len(ref)
    surv_l = len(surv)
    coef_l = len(past_coef)
    vec_l = 2*coef_l - 1

    if (coef_l != block_size):
        print("Error: block_size and coef size mismatch")
    if (ref_l != surv_l):
        print("Error: ref and surv channel size mismatch")
    if (surv_l/block_size != np.round(surv_l/block_size)):
        print("Error: surv/ref length is not an integer multiple of block_size")

    coef = np.zeros(vec_l, dtype=np.complex128)
    coef[:coef_l] = past_coef[:]
    coef_s = nfft.fft(coef)

    ref_block = np.zeros(vec_l, dtype=np.complex128)
    ref_block = ref[:vec_l]
    err_block = np.zeros(vec_l, dtype=np.complex128)
    update_block = np.zeros(vec_l, dtype=np.complex128)
    sur_block = np.zeros(coef_l, dtype=np.complex128)
    out_block = np.zeros(coef_l ,dtype=np.complex128)
    output_signal = np.zeros(surv_l, dtype=np.complex128)

    for block in range(1,np.int64(surv_l/block_size)):

        #Helper indices
        index_start = block * block_size
        index_end = (block + 1) * block_size

        #Establish Blocks
        #   Extract
        #   Pad
        #   Take FFT
        sur_block = surv[index_start:index_end]
        ref_block[:(coef_l-1)] = ref_block[coef_l:]
        ref_block[(coef_l-1):] = ref[index_start:index_end]
        ref_block_s = nfft.fft(ref_block)

        #Filter
        #   Schur product with coef in the frequency domain
        #   IFFT
        #   Extract Linear Conv section
        out_block = nfft.ifft(ref_block_s*coef_s)[(coef_l-1):]

        #Post-Processing
        #   Shift result to output buffer
        #   Compare to Surv to get the difference
        #   Pad difference with N-1 zeros at the beginning
        output_signal[index_start:index_end] = out_block[:]
        err_block[(coef_l-1):] = sur_block - out_block

        #Update coef
        #   Take FFT of padded difference
        #   Take conjugate with FFT of Input
        #   Schur product with input* and padded difference
        #   Make L-1 samples in time to zero
        #   Find mu_B, multiply by mu_B
        #   Update coef
        err_block_s = nfft.fft(err_block)
        update_block[:coef_l] = nfft.ifft(np.conj(ref_block_s)*err_block_s)[:coef_l]
        update_block_s = nfft.fft(update_block)

        mu_B = mu / (coef_l * (gamma + np.dot(np.conj(ref_block), ref_block)))
        coef_s += update_block_s * mu_B
        coef = nfft.ifft(coef_s)

    return coef[:coef_l], output_signal



def blms_step_norm (ref, surv, mu_0, beta, block_size, past_coef):
    """ Implements the fast (FFT!) block NLMS algorithm described in
            Adaptive Filters - Theory and Applications
            2nd Ed
            Behrouz Farhang-Boroujeny
            Ch 8 ("Block Implementation of Adaptive Filters")

        Let L=N, at least for now
        This version uses step normalisation as described in
            Ch 8.3.3

    And then the world will know
        and then the world will see
        and that world shall cease to be
    """
    ref_l = len(ref)
    surv_l = len(surv)
    coef_l = len(past_coef)
    vec_l = 2*coef_l - 1
    print_l = np.int64(ref_l/coef_l)

    if (coef_l != block_size):
        print("Error: block_size and coef size mismatch")
    if (ref_l != surv_l):
        print("Error: ref and surv channel size mismatch")
    if (surv_l/block_size != np.round(surv_l/block_size)):
        print("Error: surv/ref length is not an integer multiple of block_size")

    coef = np.zeros(vec_l, dtype=np.complex128)
    coef[:coef_l] = past_coef[:]
    coef_s = nfft.fft(coef)

    ref_block = np.zeros(vec_l, dtype=np.complex128)
    ref_block = ref[:vec_l]

    ref_block_p = np.ones(vec_l, dtype=np.complex128)
    mu = np.zeros(vec_l, dtype=np.complex128)
    err_block = np.zeros(vec_l, dtype=np.complex128)
    update_block = np.zeros(vec_l, dtype=np.complex128)
    sur_block = np.zeros(coef_l, dtype=np.complex128)
    out_block = np.zeros(coef_l ,dtype=np.complex128)
    output_signal = np.zeros(surv_l, dtype=np.complex128)

    value0 = np.zeros(print_l)
    value1 = np.zeros(print_l)

    for block in range(1,np.int64(surv_l/block_size)):

        #Helper indices
        index_start = block * block_size
        index_end = (block + 1) * block_size

        #Establish Blocks
        #   Extract
        #   Pad
        #   Take FFT
        sur_block = surv[index_start:index_end]
        ref_block[:(coef_l-1)] = ref_block[coef_l:]
        ref_block[(coef_l-1):] = ref[index_start:index_end]
        ref_block_s = nfft.fft(ref_block)

        #Filter
        #   Schur product with coef in the frequency domain
        #   IFFT
        #   Extract Linear Conv section
        out_block = nfft.ifft(ref_block_s*coef_s)[(coef_l-1):]

        #Post-Processing
        #   Shift result to output buffer
        #   Compare to Surv to get the difference
        #   Pad difference with N-1 zeros at the beginning
        output_signal[index_start:index_end] = out_block[:]
        err_block[(coef_l-1):] = sur_block - out_block

        #Prepare to update coef
        #   Take FFT of padded difference
        #   Take conjugate with FFT of Input
        #   Schur product with input* and padded difference
        #   Make L-1 samples in time to zero
        #   Find mu_B, multiply by mu_B
        #   Update coef
        err_block_s = nfft.fft(err_block)
        update_block[:coef_l] = nfft.ifft(np.conj(ref_block_s)*err_block_s)[:coef_l]
        update_block_s = nfft.fft(update_block)

        #Update coef
        #   update the powers associated with each coef
        #   Solve for mu_i
        #   Update coef
        ref_block_p = ref_block_p * beta + (1 - beta)*np.abs(ref_block)**2
        mu = mu_0/ref_block_p
        coef_s += update_block_s * mu
        coef = nfft.ifft(coef_s)

        value0[block] = coef[0]
        value1[block] = coef[1]

    plt.plot(value0,value1)
    plt.show()

    return coef[:coef_l], output_signal
