import stft
import peak_finding

def onsetDetection(signal):
  '''
  Returns a list of times for which the onset of the notes are at.
  '''
  