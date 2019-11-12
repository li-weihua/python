import logging
import sys

# set logging format
logging.basicConfig(
  format='%(asctime)s.%(msecs)03d %(levelname).1s %(pathname)s:%(lineno)d] %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S', 
  level=logging.INFO,
  )

def func(x, y):
  if (y != 0):
    return x/y
  else:
    raise Exception("denormator is zero!")

try:
  func(1,0)
except:
  logging.error("This message do not show traceback!")
  logging.exception("This message show traceback following:")


