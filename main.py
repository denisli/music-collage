import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from msignal import *
from similarity import *

if __name__ == '__main__':
  # get violin signals
  notes = 'abcdefg'
  SILENCE_THRESHOLD = 10
  def createInstrumentSignal(note, suffix):
    [ samplingRate, data ] = scipy.io.wavfile.read('dataset/' + note + suffix)
    data = data[abs(data) > SILENCE_THRESHOLD]
    signal = Signal(samplingRate, data[5*len(data)/16:3*len(data)/8])
    return signal
  violinSignals = map(lambda note: createInstrumentSignal(note, '_violin.wav'), notes)

  # get music signal
  musicSamplingRate, musicData = scipy.io.wavfile.read('dataset/[Boys-Over-Flowers]-Violin-Music-by-Ji-Hoo-(Full-Version).wav')
  music = Signal(musicSamplingRate, musicData[:, 0])

  # construct a new music signal using concatenated violin signals
  newMusicSamplingRate = musicSamplingRate
  signals = []
  time = 0
  while time < music.getDuration():
    print 'Progress: %d%%' % min(100, 100 * (time / music.getDuration()))
    # look for the best matching component signal
    bestMatch = None
    bestSimilarity = float('-inf')
    for violinSignal in violinSignals:
      musicTruncated = music.truncate(getIndex(music.samplingRate, time), \
        getIndex(music.samplingRate, min(music.getDuration(), time + violinSignal.getDuration())))
      violinReamplified = violinSignal.changeAmplitude(musicTruncated.getAmplitude())
      sim = similarity(musicTruncated, violinReamplified)
      if sim > bestSimilarity:
        bestSimilarity = sim
        bestMatch = violinReamplified
    signals.append(bestMatch)
    time += bestMatch.getDuration()
  newMusicData = np.concatenate( tuple(map(lambda signal: signal.data, signals)) )
  scipy.io.wavfile.write('new_music.wav', newMusicSamplingRate, newMusicData)

  # for (celloSignal, celloMark) in celloSignals:
  #   bestMatch = None
  #   bestSimilarity = float('-inf') # any number less 0 should work though
  #   for (violinSignal, violinMark) in violinSignals:
  #     sim = similarity(celloSignal, violinSignal, 0, celloSignal.getDuration(), 0, celloSignal.getDuration())
  #     if sim > bestSimilarity:
  #       bestSimilarity = sim
  #       bestMatch = (violinSignal, violinMark)
  #   print celloMark, 'best match is', bestMatch[1], 'with similarity', bestSimilarity