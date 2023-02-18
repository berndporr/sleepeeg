#!/usr/bin/python3
import matplotlib.pyplot as plt
import numpy as np
from sleepeegecg import SleepEEGECG
import datetime
import matplotlib.dates as mdates
from ecgdetectors import Detectors

myFmt = mdates.DateFormatter('%H:%M:%S')

eegecg = SleepEEGECG()

# turn it into a date/time axis
ts = []
for t in eegecg.getTimeAxis():
    customdate = datetime.datetime(1990, 1, 1, 0, 0)
    customdate = customdate + datetime.timedelta(seconds=t)
    ts.append(customdate)

tl = "time/h:m:s"

# plotting EEG
plt.title("EEG")
plt.gca().xaxis.set_major_formatter(myFmt)
plt.plot(ts,eegecg.getEEG()*1E6)
plt.xlabel(tl)
plt.ylabel("EEG/uV")

# plotting ECG
plt.figure()
plt.title("ECG")
plt.gca().xaxis.set_major_formatter(myFmt)
plt.plot(ts,eegecg.getECG())
plt.xlabel(tl)
plt.ylabel("ECG/volt")

# plotting heartrate
detectors = Detectors(eegecg.fs)
r_peaks = detectors.two_average_detector(eegecg.getECG())
r_peaks = np.array(r_peaks) / eegecg.fs
intervals = np.diff(r_peaks)
heart_rate = 60.0/intervals
ts = []
for t in r_peaks[1:]:
    customdate = datetime.datetime(2023, 1, 1, 0, 0)
    customdate = customdate + datetime.timedelta(seconds=t)
    ts.append(customdate)
plt.figure()
plt.title("Heart rate")
plt.gca().xaxis.set_major_formatter(myFmt)
plt.plot(ts, heart_rate)
plt.ylabel("Heart rate / BPM")
plt.xlabel(tl)

plt.show()
