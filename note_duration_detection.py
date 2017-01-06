import numpy as np
import stft
import numpy as np
import msignal
import scipy.io.wavfile
import matplotlib.pyplot as plt
import spectral_difference
import peak_finding
import filtering
import default_params

SILENCE_THRESHOLD = 10

def getNoteDurations(signal, onsets):
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
    # silence found at this index (but remember to check duration is at least 100)
    if i > currentOnset + 1000 and isSilent(i):
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
  sd = spectral_difference.spectralDifference(signal, default_params.WINDOW_SIZE, default_params.HOP_SIZE)
  print 'here1'
  thresholds = filtering.medianFilter(sd, default_params.MEDIAN_FILTER_KERNEL_SIZE, default_params.MEDIAN_FILTER_DELTA, default_params.MEDIAN_FILTER_LAMBDA)
  print 'here2'
  peakLocs = peak_finding.findPeaks(sd, thresholds, default_params.PEAK_FINDING_RADIUS)
  print 'here3'
  actualPeakLocs = np.multiply(peakLocs, default_params.HOP_SIZE)
  print 'here4'
  durations = getNoteDurations(signal, actualPeakLocs)
  print 'here5'
  offsets = np.add(actualPeakLocs, durations)
  print 'here6'
  plt.figure(1)
  plt.plot(signal.data, 'b')
  plt.plot(actualPeakLocs, np.zeros(len(actualPeakLocs)), 'go')
  plt.plot(offsets, np.zeros(len(offsets)), 'ro')
  plt.show()