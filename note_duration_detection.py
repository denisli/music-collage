import stft
import numpy as np
import msignal
import scipy.io.wavfile
import matplotlib.pyplot as plt
import spectral_difference
import peak_finding
import filtering
import onset_detection
import default_params
import scipy.signal

SILENCE_THRESHOLD = 500

def getNoteDurations(signal, onsets):
  durations = []
  if len(onsets) == 0: return durations
  data = np.abs(signal.data)
  n = 500
  cumulative = np.cumsum(data)
  data = (cumulative[n-1:] - cumulative[:len(cumulative)-n+1]) / n
  radius = 20
  skip = 5
  # humans can only hear onsets that are at least 60 ms apart (i.e. 60/1000 of the sampling rate indices)
  # information found in this paper:
  # https://pdfs.semanticscholar.org/5042/46e788ee540edaa03c321ca03f0e49b57b32.pdf
  # This parameter is needed cause this implementation is a bit jank and can possibly find offsets close to onset
  # Because of resolution issues, this means that there is an interval of silence. I cannot find the pitch of a
  # silent region.
  minDuration = 60 * signal.samplingRate / 1000
  def isSilent(index):
    return all(val <= SILENCE_THRESHOLD for val in data[index-radius:index+1]) or \
      all(val <= SILENCE_THRESHOLD for val in data[index:index+radius+1])
  currentOnsetIndex = 0
  currentOnset = onsets[currentOnsetIndex]
  # go through each index to see if it is a silence
  for i in xrange(radius, len(data) - radius, skip):
    if i <= currentOnset: continue # make sure index is greater than currentOnset
    # handle case where passed onto the next onset without a silence
    if currentOnsetIndex < len(onsets) - 1 and i >= onsets[currentOnsetIndex + 1]:
      durations.append(onsets[currentOnsetIndex+1] - currentOnset)
      currentOnsetIndex += 1
      if currentOnsetIndex == len(onsets): break
      currentOnset = onsets[currentOnsetIndex]
      continue
    # silence found at this index (but remember to check duration is at least 100)
    if i > currentOnset + minDuration and isSilent(i):
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
  kiki = 'dataset/Kiki-A-Town-with-an-Ocean-View.wav'
  twinkle = 'dataset/twinkle twinkle little star.wav'
  samplingRate, data = scipy.io.wavfile.read(kiki)
  print 'here0'
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  onsets = onset_detection.getOnsets(signal)
  print 'here1'
  durations = getNoteDurations(signal, onsets)
  print 'here2'
  offsets = np.add(onsets, durations)
  print 'here3'
  plt.figure(1)
  plt.plot(signal.data, 'b')
  plt.plot(onsets, np.zeros(len(onsets)), 'go')
  plt.plot(offsets, np.zeros(len(offsets)), 'ro')
  plt.show()