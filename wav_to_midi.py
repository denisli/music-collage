import midiutil.MidiFile

import numpy as np
import scipy.io.wavfile

import msignal
import onset_detection
import note_duration_detection
import pitch_detection

def monophonicWavToMidi(wav_filename, midi_filename):
  # extract wavfile information
  [ samplingRate, data ] = scipy.io.wavfile.read(wav_filename)
  data = np.sum(data, 1) # average to handle cases with more than one channel
  onsets, durations, pitches = getSignalInformation(msignal.Signal(samplingRate, data))

  # construct a midi file from the above info
  track = 0
  channel = 0
  volume = 127
  tempo = 60 # 60 beats per minute or 1 beat per second

  midi = midiutil.MidiFile.MIDIFile(adjust_origin=None)
  midi.addTempo(track, 0, tempo)
  for i in xrange(len(onsets)):
    time = float(onsets[i]) / samplingRate
    duration = float(durations[i]) / samplingRate
    # Formula for MIDI pitch in the beow wiki page
    # https://en.wikipedia.org/wiki/MIDI_Tuning_Standard
    pitch = int(69 + 12 * np.log2(float(pitches[i]) / 440))
    midi.addNote(track, channel, pitch, time, duration, volume)
  with open(midi_filename, 'wb') as output_file:
    midi.writeFile(output_file)

def getSignalInformation(signal):
  '''
  Returns the following information from a given signal:
  - note onsets
  - note durations
  - pitches
  '''
  onsets = onset_detection.getOnsets(signal)
  noteDurations = note_duration_detection.getNoteDurations(signal, onsets)
  offsets = np.add(onsets, noteDurations)
  def getPitch(index):
    return pitch_detection.getGeneralPitch(msignal.Signal(signal.samplingRate, \
      signal.truncate(onsets[index], offsets[index]).data))
  pitches = np.array([ getPitch(i) for i in xrange(len(onsets)) ])
  return onsets, noteDurations, pitches

if __name__ == '__main__':
  monophonicWavToMidi('dataset/twinkle twinkle little star.wav', 'new_music.mid')