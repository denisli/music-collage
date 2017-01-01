import matplotlib.pyplot as plt
import scipy.io.wavfile

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  plt.plot(data)
  plt.show()