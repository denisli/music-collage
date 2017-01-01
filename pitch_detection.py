import numpy as np
import stft
import numpy as np
import msignal
import scipy.io.wavfile
import matplotlib.pyplot as plt
import spectral_difference
import peak_finding
import note_duration_detection

# Implementation based off of:
# https://gerrybeauregard.wordpress.com/2013/07/15/high-accuracy-monophonic-pitch-estimation-using-normalized-autocorrelation/
# Modified accordingly by me for my own purposes
def getGeneralPitch(signal):
  '''
  Gets the single pitch that most closely matches with the signal.
  '''
  signal = signal.normalize()
  data = signal.data
  n = len(data)
  minF, maxF = 27.5, 4186.0
  minP, maxP = int(signal.samplingRate / maxF - 1), int(signal.samplingRate / minF + 1)
  bestP = minP
  bestNac = float('-inf')
  for p in xrange(minP-1, maxP+2):
    unshifted = data[:n-p].astype(float)
    shifted = data[p:n].astype(float)
    ac = np.dot(unshifted, shifted)
    sumSqBeg = np.dot(unshifted, unshifted)
    sumSqEnd = np.dot(shifted, shifted)
    nac = ac / np.sqrt(sumSqBeg * sumSqEnd)
    if nac > bestNac:
      bestNac, bestP = nac, p
  print bestP
  return float(signal.samplingRate) / bestP

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  print 'here0'
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  print 'here0.5'
  hopSize = 10
  sd = spectral_difference.spectralDifference(signal, 40, hopSize)
  print 'here1'
  thresholds = peak_finding.medianFilter(sd, 99, 0, 1)
  print 'here2'
  peakLocs = peak_finding.findPeaks(sd, thresholds, 2000)
  print 'here3'
  onsets = np.multiply(peakLocs, hopSize)
  print 'here4'
  durations = note_duration_detection.noteDurationDetection(signal, onsets)
  print 'here5'
  offsets = np.add(onsets, durations)
  print 'here6'
  getGeneralPitch(signal.truncate(onsets[9], offsets[9]+1))
