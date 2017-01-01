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
  nr, nc = absData.shape
  sd = np.empty(nr)
  for n in range(nr-1):
    diff = absData[n+1,:] - absData[n,:]
    sd[n] = np.sum(np.square((diff + np.abs(diff)) / 2))
  return sd

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  sd = spectralDifference(signal, 40, 5)
  plt.plot(sd)
  plt.show()