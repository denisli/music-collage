import stft
import numpy as np
import msignal
import scipy.io.wavfile
import scipy.signal
import matplotlib.pyplot as plt
import spectral_difference

def findPeaks(data, thresholdFunction, radius):
  peakLocs = []
  for i in xrange(len(data)):
    detection, threshold = data[i], thresholdFunction[i]
    if detection > threshold: # only accept those greater than the threshold
      left, right = max(0,i-radius), min(len(data),i+radius+1)
      if detection == np.amax(data[left:right]): # make sure that we have the max in a radius
        peakLocs.append(i)
  return np.array(peakLocs)

# Implemented using the median adaptive filter threshold shown here:
# https://pdfs.semanticscholar.org/4afa/5e20cbbc5300c51dd9e16e20674d257a3f39.pdf
def medianFilter(signal, kernelSize, delta, lamb):
  return np.add(delta, np.multiply(lamb, scipy.signal.medfilt(signal, kernelSize)))
  
if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  sd = spectral_difference.spectralDifference(signal, 40, 5)
  thresholds = medianFilter(sd, 999, 0, 1)
  plt.figure(1)
  plt.subplot(311)
  plt.plot(thresholds)
  plt.subplot(312)
  plt.plot(sd)
  plt.subplot(313)
  peakLocs = findPeaks(sd, thresholds, 2000)
  plt.plot(peakLocs, np.zeros(len(peakLocs)), 'ro')
  plt.show()