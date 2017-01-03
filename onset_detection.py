import numpy as np
import spectral_difference
import peak_finding

def getOnsets(signal):
  '''
  Returns a list of times for which the onset of the notes are at.
  '''
  hopSize = 200
  sd = spectral_difference.spectralDifference(signal, 400, hopSize)
  thresholds = peak_finding.medianFilter(sd, 1, 1e10, 0)
  peakLocs = peak_finding.findPeaks(sd, thresholds, 25)
  onsets = np.multiply(peakLocs, hopSize)
  return onsets