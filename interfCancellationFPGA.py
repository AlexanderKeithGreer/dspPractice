import sys
import os

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as ra
import scipy.signal as sig

sys.path.append(os.path.abspath("../serialFPGA"))
import serialToParallel as sp


def main():
    """Main Function, of course!"""
    #Setup
    fs = 12e6/(8*4)
    time = np.arange(0,2.2,1/fs)
    #ref = np.int16(256+256*sig.sawtooth((fs/5)*time))
    des = np.int16(np.round(512*ra.randn(len(time))))
    ref = np.int16(np.round(1024*ra.randn(len(time))))
    filt = np.array([0,0,2,-1],dtype=np.int16)
    con = np.convolve(ref,filt,mode="same") + 15 + des

    out = np.int16(0*time);
    deb = np.int16(0*time);

    #Run the data through the FPGA
    stp = sp.serial_to_parallel(12000000, "COM4", 4)
    stp.assign_stream_in([0, 1], "REF")
    stp.input_data(ref, "REF")
    stp.assign_stream_in([2, 3], "CON")
    stp.input_data(con, "CON")

    stp.assign_stream_out([0, 1], "OUT")
    stp.output_data(out, "OUT")
    stp.assign_stream_out([2, 3], "DEB")
    stp.output_data(deb, "DEB")

    stp.run()

    #Actually show it
    plt.figure()
    plt.plot(time,ref,label="ref")
    plt.plot(time,con,label="con")
    plt.plot(time,deb,label="deb")
    plt.plot(time,out,label="out")
    plt.plot(time,des,label="des")
    plt.legend()

    plt.figure()
    plt.plot(np.correlate(des,out),label="des")
    plt.plot(np.correlate(ref,out),label="ref")
    plt.legend()
    plt.show()

main()
