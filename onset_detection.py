import numpy as np
import spectral_difference
import peak_finding

def getOnsets(signal):
  '''
  Returns a list of times for which the onset of the notes are at.
  '''
  hopSize = 5
  sd = spectral_difference.spectralDifference(signal, 40, hopSize)
  thresholds = peak_finding.medianFilter(sd, 99, 0, 1)
  peakLocs = peak_finding.findPeaks(sd, thresholds, 2000)
  onsets = np.multiply(peakLocs, hopSize)
  return onsets