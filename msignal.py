import numpy as np

class Signal(object):
  def __init__(self, samplingRate, data):
    '''
    samplingRate [int] -- the sampling rate of the data
    data [ndarray] -- array containing the values of a signal at each sampling
    '''
    self.samplingRate = samplingRate
    self.data = data # TODO: should consider copying this data instead of just setting reference
  def changeSamplingRate(self, samplingRate):
    '''
    Returns a signal with desired sampling rate and correspondngly re-sampled data
    '''
    # resample the data
    data = np.interp(np.arange(0, len(self.data), float(self.samplingRate)/samplingRate), np.arange(0, len(self.data)), self.data)
    return Signal(samplingRate, data)
  def changeAmplitude(self, amplitude):
    '''
    Returns a signal with the data re-scaled by the given amplitude
    '''
    if amplitude < 0: raise RuntimeError('Amplitude was %f but must be non-negative' % amplitude)
    currentAmplitude = self.getAmplitude()
    #print np.divide(np.multiply(self.data, amplitude), currentAmplitude).dtype
    if currentAmplitude == 0: return Signal(self.samplingRate, self.data)
    else: return Signal(self.samplingRate, (self.data * float(amplitude) / currentAmplitude).astype(np.int16))
  def normalize(self):
    '''
    Returns a signal with normalized data
    '''
    
  def truncate(self, startIndex, endIndex):
    '''
    Returns a signal which matches with this signal being truncated at start index and end index
    Start index is included and end index is excluded.
    '''
    data = self.data[startIndex:endIndex]
    return Signal(self.samplingRate, data)
  def getDuration(self):
    return float(len(self.data)) / self.samplingRate
  def getAmplitude(self):
    return np.max(np.absolute(self.data))