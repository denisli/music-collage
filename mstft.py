import time
import scipy
import scipy.io.wavfile
import numpy as np
import numpy.fft
import msignal

from numpy.lib.stride_tricks import as_strided

# Implementation found here:
# http://stackoverflow.com/questions/2459295/invertible-stft-and-istft-in-python
# from the answer by Steve Tjoa
# It has been slightly modified by me.
def mstft(signal, windowSize, hopSize):
  sampingRate, data = signal.samplingRate, signal.data
  w = scipy.hanning(windowSize)
  stride = data.strides[0]
  strided = as_strided(data, shape=[(len(data)-windowSize)/hopSize, windowSize], strides=[stride*hopSize,stride])
  data = numpy.fft.fft(np.multiply(w, strided), axis=1)
  return data

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  startTime = time.time() * 1000.0
  print mstft(signal, 40, 5).shape
  endTime = time.time() * 1000.0
  print 'STFT took %d milliseconds' % (endTime - startTime)