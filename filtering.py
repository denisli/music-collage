import numpy as np
import scipy.signal

# Implemented using the median adaptive filter threshold shown here:
# https://pdfs.semanticscholar.org/4afa/5e20cbbc5300c51dd9e16e20674d257a3f39.pdf
def medianFilter(signal, kernelSize, delta, lamb):
  return np.add(delta, np.multiply(lamb, scipy.signal.medfilt(signal, kernelSize)))