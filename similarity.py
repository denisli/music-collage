import numpy as np

# Helpful links used for implementation
# http://stackoverflow.com/questions/14386130/best-way-to-compare-two-signals-in-matlab
# http://stackoverflow.com/questions/25830840/python-cross-correlation
def similarity(signal1, signal2, s1, t1, s2, t2):
  '''
  signal1 [Signal] -- first signal in a pair of signals to measure similarity for
  signal2 [Signal] -- second signal in a pair of signals to measure similarity for
  s1 [int] -- starting index of the interval in the first signal to measure similiarty (inclusive)
  t1 [int] -- ending index of the interval in the first signal to measure similarity (exclusive)
  s2 [int] -- starting index of the interval in the second signal to measure similarity (inclusive)
  t2 [int] -- ending index of the interval in the second signal to measure similarity (exclusive)
  '''
  data1, data2 = signal1.data[s1:t1], signal2.data[s2:t2]
  norm1, norm2 = np.linalg.norm(data1, ord=2), np.linalg.norm(data2, ord=2)
  normalizedData1, normalizedData2 = data1 / norm1, data2 / norm2
  correlation = np.correlate(normalizedData1, normalizedData2, 'full')
  return np.max(np.fabs(correlation))