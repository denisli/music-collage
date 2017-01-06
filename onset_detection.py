import numpy as np
import spectral_difference
import peak_finding
import filtering
import scipy.io.wavfile
import scipy.signal
import msignal
import default_params
import matplotlib.pyplot as plt

def getOnsets(signal):
  '''
  Returns a list of times for which the onset of the notes are at.
  '''
  sd = spectral_difference.spectralDifference(signal, default_params.WINDOW_SIZE, default_params.HOP_SIZE)
  sd = postProcessDetectionFunction(sd)
  thresholds = filtering.medianFilter(np.abs(sd), default_params.MEDIAN_FILTER_KERNEL_SIZE, default_params.MEDIAN_FILTER_DELTA, default_params.MEDIAN_FILTER_LAMBDA)
  peakLocs = peak_finding.findPeaks(sd, thresholds, default_params.PEAK_FINDING_RADIUS)
  onsets = np.multiply(peakLocs, default_params.HOP_SIZE)
  return onsets

def postProcessDetectionFunction(detectionFunction):
  avg = np.average(detectionFunction)
  zeroAvg = detectionFunction - avg
  amp = np.max(np.abs(zeroAvg))
  return zeroAvg / amp

if __name__ == '__main__':
  kiki = 'dataset/Kiki-A-Town-with-an-Ocean-View.wav'
  twinkle = 'dataset/twinkle twinkle little star.wav'
  samplingRate, data = scipy.io.wavfile.read(twinkle)
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  onsets = getOnsets(signal)
  plt.figure(1)
  plt.plot(data)
  plt.plot(onsets, np.zeros(len(onsets)), 'ro')
  plt.show()