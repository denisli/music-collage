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
  kiki = 'dataset/Kiki-A-Town-with-an-Ocean-View.wav'
  twinkle = 'dataset/twinkle twinkle little star.wav'
  samplingRate, data = scipy.io.wavfile.read(twinkle)
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  hopSize = 200
  sd = spectral_difference.spectralDifference(signal, 400, hopSize)
  sdUpsampled = scipy.signal.resample(sd, len(sd) * hopSize)
  thresholds = medianFilter(sd, 1, 1e10, 0)
  peakLocs = findPeaks(sd, thresholds, 25)
  onsets = peakLocs * hopSize
  plt.figure(1)
  plt.subplot(211)
  plt.plot(sdUpsampled)
  plt.subplot(212)
  plt.plot(data)
  plt.plot(onsets, np.zeros(len(peakLocs)), 'ro')
  plt.show()