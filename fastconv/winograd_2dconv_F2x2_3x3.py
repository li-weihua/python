"""
 2d winograd F(2x2, 3x3) convolution
 todo: image padding and image height or width is even
"""

import numpy as np
from scipy.signal import correlate2d as _correlate2d

def conv2d(img, kernel):
  """
  native 2d convolution, no padding, stride is 1
  """
  assert len(img.shape) == 4
  assert len(kernel.shape) == 4
  
  (N, C, H, W) = img.shape
  (K, C, S, R) = kernel.shape
  
  LX = W - R + 1
  LY = H - S + 1
  
  out = np.zeros([N, K, LY, LX])
    
  for k in range(K):
    for n in range(N):
      for c in range(C):
        out[n, k] += _correlate2d(img[n, c], kernel[k, c], mode='valid')
    
  return out

def transform_kernel(g):
  """
  calculate U_{k,c} = GgG'
  convolution kernel is (K, C, R, S)
      K: filter number
      C: channel number
      R: filter height
      S: filter weidth
  R = S = 3
  """
  (K, C) = g.shape[0:2]
  U = np.zeros([K, C, 4, 4])
  
  G = np.array([[1, 0, 0],
                [0.5, 0.5, 0.5],
                [0.5, -0.5, 0.5],
                [0, 0, 1]])
  for k in range(K):
    for c in range(C):
      U[k, c] = G@g[k, c]@G.T
  return U

# calculate V = B'dB
def tansform_pixel_tile(d):
  """ matrix multiply
  BT = np.array([[1,0,-1,0],
                 [0,1,1,0],
                 [0,-1,1,0],
                 [0,1,0,-1]])
  return BT@d@BT.T
  """
  x = np.zeros([4, 4])

  for i in range(4):
    x[0, i] = d[0, i] - d[2, i]
    x[1, i] = d[1, i] + d[2, i]
    x[2, i] = d[2, i] - d[1, i]
    x[3, i] = d[1, i] - d[3, i]
  
  V = np.zeros([4, 4])
  for i in range(4):
    V[i, 0] = x[i, 0] - x[i, 2]
    V[i, 1] = x[i, 1] + x[i, 2]
    V[i, 2] = x[i, 2] - x[i, 1]
    V[i, 3] = x[i, 1] - x[i, 3]    
  
  return V


def winograd_conv2d_F2x2_3x3(img, kernel):
  """
  input img format is NCHW
  assume H and W is even!
  """
  assert len(img.shape) == 4
  assert len(kernel.shape) == 4
  
  (N, C, H, W) = img.shape
  (K, C, S, R) = kernel.shape

  U = transform_kernel(kernel)
  
  LX = W - R + 1
  LY = H - S + 1
  
  out = np.zeros([N, K, LY, LX])
  
  RX = LX % 2
  RY = LY % 2
  t = np.zeros([2, 4])
  
  for k in range(K):
    for c in range(C):
      for n in range(N):
        for ytile in range(LY//2):
          for xtile in range(LX//2):
            d = img[n, c, 2*ytile:2*ytile+4, 2*xtile:2*xtile+4]
            V = tansform_pixel_tile(d)
            
            V = U[k, c]*V      
            for i in range(4):
              t[0, i] = V[0, i] + V[1, i] + V[2, i]
              t[1, i] = V[1, i] - V[2, i] - V[3, i]
            
            out[n, k, 2*ytile:2*ytile+2, 2*xtile:2*xtile+2] += np.array([
                [t[0,0] + t[0,1] + t[0,2], t[0,1] - t[0,2] - t[0,3] ],
                [t[1,0] + t[1,1] + t[1,2], t[1,1] - t[1,2] - t[1,3] ] ])
      
  return out

if __name__ == "__main__":

  W = 6
  C = 2
  K = 3
  img = np.random.rand(1, C, W, W)
  kernel =  np.random.rand(K, C, 3, 3)

  res_native = conv2d(img, kernel)
  res_winograd = winograd_conv2d_F2x2_3x3(img, kernel)

  #"""
  print("native convolution")
  print(res_native)
  print("")
  print("winograd convolution")
  print(res_winograd)
  print("")
  #"""

  if np.max(np.abs(res_native - res_winograd)) < 1e-4 :
    print("check OK!")
  else:
    print("check wrong!")