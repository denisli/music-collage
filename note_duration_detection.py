import numpy as np
import stft
import numpy as np
import msignal
import scipy.io.wavfile
import matplotlib.pyplot as plt
import spectral_difference
import peak_finding

SILENCE_THRESHOLD = 10

def noteDurationDetection(signal, onsets):
  durations = []
  if len(onsets) == 0: return durations
  absData = np.abs(signal.data)
  radius = 20
  skip = 50
  def isSilent(index):
    return all(val <= SILENCE_THRESHOLD for val in absData[index-radius:index+1]) or \
      all(val <= SILENCE_THRESHOLD for val in absData[index:index+radius+1])
  currentOnsetIndex = 0
  currentOnset = onsets[currentOnsetIndex]
  # go through each index to see if it is a silence
  for i in xrange(radius, len(absData) - radius, skip):
    if i <= currentOnset: continue # make sure index is greater than currentOnset
    # handle case where passed onto the next onset without a silence
    if currentOnsetIndex < len(onsets) - 1 and i >= onsets[currentOnsetIndex + 1]:
      durations.append(onsets[currentOnsetIndex+1] - currentOnset)
      currentOnsetIndex += 1
      if currentOnsetIndex == len(onsets): break
      currentOnset = onsets[currentOnsetIndex]
      continue
    # silence found at this index
    if isSilent(i):
      durations.append(i - currentOnset + 1)
      currentOnsetIndex += 1
      if currentOnsetIndex == len(onsets): break
      currentOnset = onsets[currentOnsetIndex]
      continue
  # handle the case where the signal ends without a silence (i.e. in the middle of a note)
  if currentOnsetIndex == len(onsets) - 1:
    durations.append(len(onsets) - currentOnset)
  return np.array(durations)

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  print 'here0'
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  hopSize = 10
  sd = spectral_difference.spectralDifference(signal, 40, hopSize)
  print 'here1'
  thresholds = peak_finding.medianFilter(sd, 99, 0, 1)
  print 'here2'
  peakLocs = peak_finding.findPeaks(sd, thresholds, 2000)
  print 'here3'
  actualPeakLocs = np.multiply(peakLocs, hopSize)
  print 'here4'
  durations = noteDurationDetection(signal, actualPeakLocs)
  print 'here5'
  offsets = np.add(actualPeakLocs, durations)
  print 'here6'
  plt.figure(1)
  plt.plot(signal.data, 'b')
  plt.plot(actualPeakLocs, np.zeros(len(actualPeakLocs)), 'go')
  plt.plot(offsets, np.zeros(len(offsets)), 'ro')
  plt.show()