# ===================================================================
#  Pitch detection module
#
#  Demonstrates use of period estimator algorithm based on 
#  normalized autocorrelation. Other neat tricks include sub-sample
#  accuracy of the period estimate, and avoidance of octave errors.
#
#  Released under the MIT License
#
#  The MIT License (MIT)
#
#  Copyright (c) 2017 Denis Li
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
# ===================================================================

import numpy as np
import stft
import numpy as np
import msignal
import scipy.io.wavfile
import matplotlib.pyplot as plt
import spectral_difference
import peak_finding
import note_duration_detection

# Implementation based off of:
# https:#gerrybeauregard.wordpress.com/2013/07/15/high-accuracy-monophonic-pitch-estimation-using-normalized-autocorrelation/
# Modified accordingly by me for my own purposes
def getGeneralPitch(signal):
  '''
  Gets the single pitch that most closely matches with the signal.
  '''
  signal = signal.normalize()
  data = signal.data
  n = len(data)
  minF, maxF = 27.5, 4186.0
  minP, maxP = int(signal.samplingRate / maxF - 1), int(signal.samplingRate / minF + 1)
  
  # figure out the normalized autocorrelation
  nac = np.zeros(maxP + 2).astype(float)
  for p in xrange(minP-1, maxP+2):
    unshifted = data[:n-p].astype(float)
    shifted = data[p:n].astype(float)
    ac = np.dot(unshifted, shifted)
    sumSqBeg = np.dot(unshifted, unshifted)
    sumSqEnd = np.dot(shifted, shifted)
    nac[p] = ac / np.sqrt(sumSqBeg * sumSqEnd)

  # find the highest value
  bestP = minP
  for p in xrange(minP, maxP+1):
    if nac[p] > nac[bestP]: bestP = p

  # interpolate to find the estimated period
  mid, left, right = nac[bestP], nac[bestP-1], nac[bestP+1]
  shift = 0.5 * (right - left) / (2 * mid - left - right)
  pEst = bestP + shift

  # find out if there is a sub-multiple period that works
  subMulThreshold = 0.9
  maxMul = bestP / minP
  found = False
  mul = maxMul
  while not found and mul >= 1:
    subsAllStrong = True
    pTest = pEst / mul
    for k in xrange(1, mul):
      pTestMul = int(k * pTest + 0.5)
      if nac[pTestMul] < subMulThreshold * nac[bestP]: subsAllStrong = False
    if subsAllStrong:
      found = True
      pEst = pTest
    mul -= 1
  return float(signal.samplingRate / pEst)

if __name__ == '__main__':
  samplingRate, data = scipy.io.wavfile.read('dataset/twinkle twinkle little star.wav')
  print 'here0'
  data = np.sum(data, 1)
  signal = msignal.Signal(samplingRate, data)
  print 'here0.5'
  hopSize = 10
  sd = spectral_difference.spectralDifference(signal, 40, hopSize)
  print 'here1'
  thresholds = peak_finding.medianFilter(sd, 99, 0, 1)
  print 'here2'
  peakLocs = peak_finding.findPeaks(sd, thresholds, 2000)
  print 'here3'
  onsets = np.multiply(peakLocs, hopSize)
  print 'here4'
  durations = note_duration_detection.getNoteDurations(signal, onsets)
  print 'here5'
  offsets = np.add(onsets, durations)
  print 'here6'
  for i in xrange(len(onsets)):
    print i, getGeneralPitch(signal.truncate(onsets[i], offsets[i]+1))
