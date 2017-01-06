import stft
import numpy as np
import msignal
import scipy.io.wavfile
import scipy.signal
import matplotlib.pyplot as plt
import spectral_difference
import filtering
import default_params

def findPeaks(data, thresholdFunction, radius):
  peakLocs = []
  for i in xrange(len(data)):
    detection, threshold = data[i], thresholdFunction[i]
    if detection > threshold: # only accept those greater than the threshold
      left, right = max(0,i-radius), min(len(data),i+radius+1)
      if detection == np.amax(data[left:right]): # make sure that we have the max in a radius
        peakLocs.append(i)
  return np.array(peakLocs)
  
if __name__ == '__main__':
  kiki = 'dataset/Kiki-A-Town-with-an-Ocean-View.wav'
  twinkle = 'dataset/twinkle twinkle little star.wav'
  samplingRate, data = scipy.io.wavfile.read(twinkle)
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  sd = spectral_difference.spectralDifference(signal, default_params.WINDOW_SIZE, default_params.HOP_SIZE)
  sdUpsampled = scipy.signal.resample(sd, len(sd) * default_params.HOP_SIZE)
  thresholds = filtering.medianFilter(sd, default_params.MEDIAN_FILTER_KERNEL_SIZE, default_params.MEDIAN_FILTER_DELTA, default_params.MEDIAN_FILTER_LAMBDA)
  peakLocs = findPeaks(sd, thresholds, default_params.PEAK_FINDING_RADIUS)
  onsets = peakLocs * default_params.HOP_SIZE
  plt.figure(1)
  plt.subplot(211)
  plt.plot(sdUpsampled)
  plt.subplot(212)
  plt.plot(data)
  plt.plot(onsets, np.zeros(len(peakLocs)), 'ro')
  plt.show()