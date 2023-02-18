#!/usr/bin/python
import numpy as np
from scipy import signal

class SleepEEGECG:
    """
    Class which loads the EEG/ECG recording and you can then access the
    data then via its methods.
    """
    fs = 1.0/0.003
    def __init__(self):
        s = 2.5/256/10000
        v = np.loadtxt("eeg_c.dat")[:,0]
        w = np.loadtxt("eeg_c.dat")[:,1]
        v = v * s
        w = w / 1E5
        # highpass Butterworth filter
        cutoff = 0.25
        # create a 4th order highpass
        b, a = signal.butter(2, cutoff/self.fs*2.0, 'highpass')
        # filter the signal adc1
        v = signal.lfilter(b, a, v)
        # filter the signal adc2
        w = signal.lfilter(b, a, w)
        # create a 2nd order order stopband filter at 50Hz
        # to remove the 50Hz mains
        f1 = 45
        f2 = 55
        b, a = signal.butter(2, [f1/self.fs*2.0, f2/self.fs*2.0 ], 'bandstop')
        # filter the 1st ADC channel
        self.eeg = signal.lfilter(b, a, v)
        self.ecg = signal.lfilter(b, a, w)

    def getTimeAxis(self):
        """
        Returns a numpy array of the time axis in seconds of the whole recording.
        """
        return np.linspace(0,(len(self.eeg)/self.fs),len(self.eeg))

    def getEEG(self):
        """
        Returns the EEG data in volt.
        """
        return self.eeg

    def getECG(self):
        """
        Returns the ECG data in mV. Note that the amplifier was not calibrated so its only approximate.
        """
        return self.ecg
