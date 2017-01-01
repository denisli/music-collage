import stft
import numpy as np
import msignal
import scipy.io.wavfile
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
def thresholdFunction(detectionFunction, delta, lamb, M):
  def adaptiveThreshold(n):
    left, right = max(0, n-M), min(len(detectionFunction), n+M+1)
    return delta + lamb * np.median(np.abs(detectionFunction[left:right]))
  return np.array( [ adaptiveThreshold(n) for n in xrange(len(detectionFunction)) ] )
  
if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  sd = spectral_difference.spectralDifference(signal, 40, 5)
  thresholds = thresholdFunction(sd, 0, 1, 1000)
  plt.figure(1)
  plt.subplot(311)
  plt.plot(thresholds)
  plt.subplot(312)
  plt.plot(sd)
  plt.subplot(313)
  peakLocs = findPeaks(sd, thresholds, 2000)
  plt.plot(peakLocs, np.zeros(len(peakLocs)), 'ro')
  plt.show()