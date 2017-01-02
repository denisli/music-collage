import time
import stft
import numpy as np
import msignal
import scipy.io.wavfile
import matplotlib.pyplot as plt

# Implementation information found here:
# http://bingweb.binghamton.edu/~ahess2/Onset_Detection_Nov302011.pdf
# Modified by me
def spectralDifference(signal, windowSize, hopSize):
  stftData = stft.stft(signal, windowSize, hopSize)
  absData = np.abs(stftData)
  diff = np.diff(absData, axis=0)
  sd = np.sum(np.square(np.divide(np.add(diff, np.abs(diff)), 2)), 1)
  return sd

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  startTime = time.time()*1000.0
  sd = spectralDifference(signal, 40, 5)
  endTime = time.time()*1000.0
  print 'spectralDifference() took %d milliseconds' % (endTime - startTime)
  plt.plot(sd)
  plt.show()