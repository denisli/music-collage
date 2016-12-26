import math

def getTime(samplingRate, index):
  return float(index) / samplingRate

def getIndex(samplingRate, time):
  return int(math.floor(float(time) * samplingRate))