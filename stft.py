import scipy
import scipy.io.wavfile
import numpy as np
import msignal

# Implementation found here:
# http://stackoverflow.com/questions/2459295/invertible-stft-and-istft-in-python
# from the answer by Steve Tjoa
# It has been slightly modified by me.
def stft(signal, windowSize, hopSize):
  sampingRate, data = signal.samplingRate, signal.data
  w = scipy.hanning(windowSize)
  data = scipy.array([scipy.fft(w*data[i:i+windowSize]) for i in range(0, len(data)-windowSize, hopSize)])
  return data

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  data = np.add(data[:,0], data[:,1])
  signal = msignal.Signal(samplingRate, data)
  print stft(signal, 40, 5).shape