import numpy as np
import spectral_difference
import peak_finding
import default_params

def getOnsets(signal):
  '''
  Returns a list of times for which the onset of the notes are at.
  '''
  sd = spectral_difference.spectralDifference(signal, default_params.WINDOW_SIZE, default_params.HOP_SIZE)
  thresholds = peak_finding.medianFilter(sd, default_params.MEDIAN_FILTER_KERNEL_SIZE, default_params.MEDIAN_FILTER_DELTA, default_params.MEDIAN_FILTER_LAMBDA)
  peakLocs = peak_finding.findPeaks(sd, thresholds, default_params.PEAK_FINDING_RADIUS)
  onsets = np.multiply(peakLocs, default_params.HOP_SIZE)
  return onsets