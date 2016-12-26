import numpy as np
from signal_util import *

# Helpful links used for implementation
# http://stackoverflow.com/questions/14386130/best-way-to-compare-two-signals-in-matlab
# http://stackoverflow.com/questions/25830840/python-cross-correlation
def similarity(signal1, signal2):
  '''
  Gets the similarity of two signals. The two signals are expected to be at the same
  sampling rate.

  signal1 [Signal] -- first signal in a pair of signals to measure similarity for
  signal2 [Signal] -- second signal in a pair of signals to measure similarity for
  '''
  if signal1.samplingRate != signal2.samplingRate:
    raise RuntimeError('similarity: Sampling rates of the two must be the same, but they are 1) %f and 2) %f' % \
      (signal1.samplingRate, signal2.samplingRate))
  data1, data2 = signal1.data, signal2.data
  norm1, norm2 = np.linalg.norm(data1, ord=2), np.linalg.norm(data2, ord=2)
  normalizedData1, normalizedData2 = data1 / norm1, data2 / norm2
  correlation = np.correlate(normalizedData1, normalizedData2, 'full')
  return np.max(np.fabs(correlation))