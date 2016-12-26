import scipy.io.wavfile
from msignal import *
from similarity import *

if __name__ == '__main__':
  [ samplingRate1, data1 ] = scipy.io.wavfile.read('test.wav')
  [ samplingRate2, data2 ] = scipy.io.wavfile.read('test2.wav')
  signal1 = Signal(samplingRate1, data1)
  signal2 = Signal(samplingRate2, data2)
  print similarity(signal1, signal2, 0, len(data1), 0, len(data2))