class Signal(object):
  def __init__(self, samplingRate, data):
    '''
    samplingRate [int] -- the sampling rate of the data
    data [ndarray] -- array containing the values of a signal at each sampling
    '''
    self.samplingRate = samplingRate
    self.data = data # TODO: should consider copying this data instead of just setting reference