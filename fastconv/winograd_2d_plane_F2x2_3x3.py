# 2d plane 2d winograd

import numpy as np
from scipy.signal import correlate2d

# calculate U = GgG'
def transform_kernel(g):
  G = np.array([[1, 0, 0],
                [0.5, 0.5, 0.5],
                [0.5, -0.5, 0.5],
                [0, 0, 1]])
  return G@g@G.T

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


#winograd 2d plane convolution, no padding
def winograd_2dconv_F2x2_3x3(img, kernel):
  (H, W) = img.shape
  (S, R) = kernel.shape

  U = transform_kernel(kernel)

  """
  AT = np.array([[1, 1, 1, 0],
                 [0, 1, -1, -1]])
  A = AT.T
  """
  
  LX = W - R + 1
  LY = H - S + 1
  
  out = np.zeros([LY, LX])
  
  RX = LX % 2
  RY = LY % 2
  t = np.zeros([2, 4])
  
  for ytile in range(LY//2):
    for xtile in range(LX//2):
      d = img[2*ytile:2*ytile+4, 2*xtile:2*xtile+4]
      V = tansform_pixel_tile(d)
      
      V = U*V      
      for i in range(4):
        t[0, i] = V[0, i] + V[1, i] + V[2, i]
        t[1, i] = V[1, i] - V[2, i] - V[3, i]
      
      out[2*ytile:2*ytile+2, 2*xtile:2*xtile+2] = np.array([
          [t[0,0] + t[0,1] + t[0,2], t[0,1] - t[0,2] - t[0,3] ],
          [t[1,0] + t[1,1] + t[1,2], t[1,1] - t[1,2] - t[1,3] ] ])
      #out[2*ytile:2*ytile+2, 2*xtile:2*xtile+2] = AT@(U*V)@A
      
  return out

if __name__ == "__main__":

  N = 8
  img = np.random.rand(N, N)
  kernel =  np.random.rand(3,3)

  res_native = correlate2d(img, kernel, mode='valid')
  res_winograd = winograd_2dconv_F2x2_3x3(img, kernel)

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