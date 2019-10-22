from __future__ import absolute_import
import numpy as _np

class var:
    def __init__(self, val, dot):
        self.val = val
        if isinstance(dot, list):
            dot = _np.array(dot, dtype='float64')
        elif isinstance(dot, _np.ndarray):
            pass
        else:
            raise NotImplementedError("not implement!")

        self.dot = dot

    def __neg__(self):
        return var(-self.val, -self.dot)

    def __abs__(self):
        if (self.val >= 0):
            return self
        else:
            return -self

    def __add__(self, v):
        if isinstance(v, var):
            return var(self.val + v.val, self.dot + v.dot)
        elif isinstance(v, (int, float)):
            return var(self.val + v, self.dot)
        else:
            raise NotImplementedError("not implement!")

    def __radd__(self, v):
        if isinstance(v, (int, float)):
            return var(v + self.val, self.dot)
        else:
            raise NotImplementedError("not implement!")

    def __sub__(self, v):
        if isinstance(v, var):
            return var(self.val - v.val, self.dot - v.dot)
        elif isinstance(v, (int, float)):
            return var(self.val - v, self.dot)
        else:
            raise NotImplementedError("not implement!")

    def __rsub__(self, v):
        if isinstance(v, (int, float)):
            return var(v - self.val , -self.dot)
        else:
            raise NotImplementedError("not implement!")

    def __mul__(self, v):
        if isinstance(v, var):
            return var(self.val*v.val, self.val*v.dot + self.dot*v.val)
        elif isinstance(v, (int, float)):
            return var(self.val * v, self.dot * v)
        else:
            raise NotImplementedError("not implement!")

    def __rmul__(self, v):
        if isinstance(v, (int, float)):
            return var(v, self.val, v * self.dot)
        else:
            raise NotImplementedError("not implement!")

    def __truediv__(self, v):
        if isinstance(v, var):
            return var(self.val/v.val, self.dot/v.val - 
                    self.val*v.dot/v.val**2)
        elif isinstance(v, (int, float)):
            return var(self.val / v, self.dot / v)
        else:
            raise NotImplementedError("not implement!")

    def __rtruediv__(self, v):
        if isinstance(v, (int, float)):
            return var(v / self.val, - v /self.val**2 * self.dot)
        else:
            raise NotImplementedError("not implement!")


    def __pow__(self, v):
        if isinstance(v, var):
            return var(self.val**v.val, self.val**v.val * (
                v.dot*_np.log(self.val) + v.val/self.val))
        elif isinstance(v, (int, float)):
            return var(self.val**v, v * self.val**(v-1) * self.dot)
        else:
            raise NotImplementedError("not implement!")

    def __rpow__(self, v):
        if isinstance(v, (int, float)):
            return var(v**self.val, v**self.val * _np.log(v))
        else:
            raise NotImplementedError("not implement!")



