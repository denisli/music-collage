import scipy.io.wavfile
from msignal import *
from similarity import *

if __name__ == '__main__':
  notes = 'abcdefg'
  def createInstrumentSignal(note, suffix):
    [ samplingRate, data ] = scipy.io.wavfile.read('dataset/' + note + suffix)
    signal = Signal(samplingRate, data)
    return signal
  celloSignals = map(lambda note: (createInstrumentSignal(note, '_cello.wav'), note), notes)
  violinSignals = map(lambda note: (createInstrumentSignal(note, '_violin.wav'), note), notes)
  for (celloSignal, celloMark) in celloSignals:
    bestMatch = None
    bestSimilarity = float('-inf') # any number less 0 should work though
    for (violinSignal, violinMark) in violinSignals:
      sim = similarity(celloSignal, violinSignal, 0, celloSignal.getDuration() / 4, 0, celloSignal.getDuration() / 4)
      if sim > bestSimilarity:
        bestSimilarity = sim
        bestMatch = (violinSignal, violinMark)
    print celloMark, 'best match is', bestMatch[1], 'with similarity', bestSimilarity