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
    Changes the sampling rate to a desired value and modifies the data correspondingly
    '''
    # resample the data
    self.data = np.interp(np.arange(0, len(self.data), float(self.samplingRate)/samplingRate), np.arange(0, len(self.data)), self.data)
    self.samplingRate = samplingRate
  def getDuration(self):
    return float(len(self.data)) / self.samplingRate