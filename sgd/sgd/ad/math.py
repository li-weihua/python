from __future__ import absolute_import
import numpy as _np
from .ad import var

def sin(x):
    if isinstance(x, var):
        return var(_np.sin(x.val), _np.cos(x.val) * x.dot)
    elif isinstance(x, (int, float)):
        return _np.sin(x)
    else:
        raise NotImplementedError("not implement!")

def cos(x):
    if isinstance(x, var):
        return var(_np.cos(x.val), - _np.sin(x.val) * x.dot)
    elif isinstance(x, (int, float)):
        return _np.cos(x)
    else:
        raise NotImplementedError("not implement!")

def log(x):
    if isinstance(x, var):
        return var(_np.log(x.val), x.dot / x.val)
    elif isinstance(x, (int, float)):
        return _np.log(x)
    else:
        raise NotImplementedError("not implement!")



