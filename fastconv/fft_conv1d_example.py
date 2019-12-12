import numpy as np
from numpy.fft import fft
from numpy.fft import ifft
from scipy.signal import convolve

"""
signal and filter are both 1d
signal length is L
filter length is M
result of linear/full convolution length is L+M-1
result of circular/valid convolution length is L-M+1
result of same convolution length is L-M+1
In general, when stride = 1, the output size is L-M+2p+1
"""

# linear convolution, padding with p = M-1
def LinearConv(x, k):
    return convolve(x, k, 'full')

# valid convolution, also no padding
def CircularConv(x, k):
    return convolve(x, k, 'valid')

# save convolution, padding with p = (M-1)/2
def SameConv(x, k):
    return convolve(x, k, 'same')


# We need zero padding the signal filter ending,
# and the length must be at least L + M -1.
# extpad means extra padding at the end of signal and filter
def FFTLinearConv(x, k, extpad = 0):
    assert len(x.shape) == 1
    assert len(k.shape) == 1
    assert extpad >= 0

    L = x.shape[0]
    M = k.shape[0]
    T0 = L + M - 1
    T = T0 + extpad
    return np.real(ifft(fft(x, T) * fft(k, T)))[0:T0]

# valid convolution donot need padding signal
# extpad means extra padding at the end of signal and filter
def FFTCircularConv(x, k, extpad = 0):
    assert len(x.shape) == 1
    assert len(k.shape) == 1
    assert extpad >= 0

    L = x.shape[0]
    M = k.shape[0]
    T0 = L - M + 1
    T = L + extpad
    return np.real(ifft(fft(x, T) * fft(k, T)))[M-1: M-1+T0]

def FFTCircularConv2(x, k, extpad = 0):
    assert len(x.shape) == 1
    assert len(k.shape) == 1
    assert extpad >= 0

    L = x.shape[0]
    M = k.shape[0]
    T0 = L - M + 1
    T = L + M - 1 + extpad
    return np.real(ifft(fft(x, T) * fft(k, T)))[M-1: M-1+T0]


# We need zero padding the signal filter ending,
# and the length must be at least L + M -1.
# extpad means extra padding at the end of signal and filter
def FFTSameConv(x, k, extpad = 0):
    assert len(x.shape) == 1
    assert len(k.shape) == 1
    assert extpad >= 0

    L = x.shape[0]
    M = k.shape[0]
    T0 = L 
    T = L + M - 1 + extpad
    return np.real(ifft(fft(x, T) * fft(k, T)))[(M-1)//2: (M-1)//2 + T0]


# check the result
def CheckResult(x, y, tol = 1e-4):
    assert x.shape == y.shape
    assert x.size == y.size
    if np.max(np.abs(x-y)) <= tol:
        return True
    else:
        return False

if __name__ == "__main__":
    L = 10
    M = 3
    x = np.random.random(L)
    k = np.random.random(M)
    conv1 = LinearConv(x, k)
    conv2 = FFTLinearConv(x, k, 3)
    conv3 = CircularConv(x, k)
    conv4 = FFTCircularConv2(x, k, 3)
    conv5 = SameConv(x, k)
    conv6 = FFTSameConv(x, k, 3)

    print("signal:\n", x)
    print("filter:\n", k)
    print("LinearConv:\n", conv1)
    print("FFTLinearConv:\n", conv2)
    print("CircularConv:\n", conv3)
    print("FFTCircularConv:\n", conv4)
    print("SameConv:\n", conv5)
    print("FFTSameConv:\n", conv6)

    if CheckResult(conv1, conv2):
        print("Check LinearConv success.")
    else:
        print("Check LinearConv fail!")

    if CheckResult(conv3, conv4):
        print("Check CircularConv success.")
    else:
        print("Check FFTCircularConv fail!")

    if CheckResult(conv5, conv6):
        print("Check SameConv success.")
    else:
        print("Check FFTSameConv fail!")

