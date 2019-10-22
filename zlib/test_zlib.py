import zlib

import cv2
import numpy as np
import time

# read image
img = cv2.imread('./house.tif', 0)
dsize = img.size
img = img.reshape([img.size])

# compress, default level
t1 = time.perf_counter()
compressed_data = zlib.compress(img.data)
t2 = time.perf_counter()
print(f'compression rate: {len(img.data)/len(compressed_data)}')
print(f'compression speed: {dsize/1024/((t2-t1)*1000)} MB/s')

# decompress data
t1 = time.perf_counter()
data = zlib.decompress(compressed_data)
t2 = time.perf_counter()
print(f'decompression speed: {dsize/102/((t2-t1)*1000)} MB/s')

data = np.frombuffer(data, dtype=np.uint8)

# do check
print(np.array_equal(img, data))
