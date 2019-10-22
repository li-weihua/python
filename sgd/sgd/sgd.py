#!/usr/bin/env python3
#%matplotlib qt5

#import my own autograd (only forward mode for now!) library
import ad 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.colors import LogNorm
from collections import defaultdict
from itertools import zip_longest

class TrajectoryAnimation(animation.FuncAnimation):
    
    def __init__(self, *paths, labels=[], fig=None, ax=None, frames=None, 
                 interval=25, repeat_delay=50, blit=True, **kwargs):

        if fig is None:
            if ax is None:
                fig, ax = plt.subplots()
            else:
                fig = ax.get_figure()
        else:
            if ax is None:
                ax = fig.gca()

        self.fig = fig
        self.ax = ax
        
        self.paths = paths

        if frames is None:
            frames = max(path.shape[1] for path in paths)
  
        self.lines = [ax.plot([], [], label=label, lw=2)[0] 
                      for _, label in zip_longest(paths, labels)]
        self.points = [ax.plot([], [], 'o', color=line.get_color())[0] 
                       for line in self.lines]

        super(TrajectoryAnimation, self).__init__(fig, self.animate, init_func=self.init_anim,
                                                  frames=frames, interval=interval, blit=blit,
                                                  repeat_delay=repeat_delay, **kwargs)

    def init_anim(self):
        for line, point in zip(self.lines, self.points):
            line.set_data([], [])
            point.set_data([], [])
        return self.lines + self.points

    def animate(self, i):
        for line, point, path in zip(self.lines, self.points, self.paths):
            line.set_data(*path[::,:i])
            point.set_data(*path[::,i-1:i])
        return self.lines + self.points

##
lossfunc  = lambda x, y: (1.5 - x + x*y)**2 + (2.25 - x + x*y**2)**2 + (2.625 - x + x*y**3)**2

xmin, xmax, xstep = -4., 4., .2
ymin, ymax, ystep = -4., 4., .2

x, y = np.meshgrid(np.arange(xmin, xmax + xstep, xstep), np.arange(ymin, ymax + ystep, ystep))
z = lossfunc(x, y)

minima_ = np.array([3., 0.5]).T

# calculate the grad
def grad(func, x):
    x1 = ad.var(x[0], [1,0])
    x2 = ad.var(x[1], [0,1])
    return func(x1, x2).dot

methods = []

x0 = np.array([1.1, 1.95])

#SGD
def SGD(func, x0, path =[], eta = 1e-3, nIter = 200, tol = 1e-3):
    x = x0
    path.append(x)
    
    for i in range(nIter):
        dx = grad(func, x)
        x = x - eta * dx  
        path.append(x)
        
        if (dx.dot(dx) < tol):
            break

methods.append(SGD.__name__)

#MomentumSGD
def MomentumSGD(func, x0, path =[], eta = 1e-3, beta = 0.9, nIter = 200, tol = 1e-3):
    x = x0
    momentum = np.zeros(x0.shape)
    path.append(x0)
    
    for i in range(nIter):
        dx = grad(func, x)
        momentum = beta * momentum - eta * dx
        x = x + momentum
        path.append(x)
    
        if (dx.dot(dx) < tol):
            break

methods.append(MomentumSGD.__name__)


#NAG
def NAG(func, x0, path =[], eta = 1e-3, beta = 0.9, nIter = 200, tol = 1e-3):
    x = x0
    momentum = np.zeros(x0.shape)
    path.append(x0)
    
    for i in range(nIter):        
        xp = x + beta * momentum
        dxp = grad(func, xp)
        
        momentum = beta * momentum - eta * dxp
        x = x + momentum
        path.append(x)
    
        if (dxp.dot(dxp) < tol):
            break

methods.append(NAG.__name__)

#Adagrad
def Adagrad(func, x0, path =[], eta = 1.2, epsilon=1e-8, nIter = 200, tol = 1e-3):
    x = x0
    path.append(x0)
    gradsum = np.zeros(x0.shape)
    
    for i in range(nIter):
        dx = grad(func, x)        
        gradsum = gradsum + dx**2        
        x = x -eta * dx /(np.sqrt(gradsum) + epsilon)
        path.append(x)
    
        if (dx.dot(dx) < tol):
            break

methods.append(Adagrad.__name__)

#RMSprop
def RMSprop(func, x0, path =[], eta = 0.1, beta = 0.9, epsilon=1e-8, 
        nIter = 200, tol = 5e-3):
    x = x0
    path.append(x0)
    
    gradsum = np.zeros(x0.shape)
    
    for i in range(nIter):
        dx = grad(func, x)        
        gradsum = beta * gradsum + (1 - beta) * dx**2
        x = x -eta * dx /(np.sqrt(gradsum) + epsilon)
        path.append(x)
    
        if (dx.dot(dx) < tol):
            break


methods.append(RMSprop.__name__)


#Adadelta
def Adadelta(func, x0, path =[], beta = 0.2, epsilon = 1e-3, 
        nIter = 200, tol = 5e-3):
    x = x0    
    path.append(x0)
    
    gradsum = np.zeros(x0.shape)       
    xsum = np.zeros(x0.shape)    
    
    for i in range(nIter):
        dx = grad(func, x)       
        gradsum = beta * gradsum + (1 - beta) * dx**2
        deltax = - (np.sqrt(xsum) + epsilon) / (np.sqrt(gradsum) + epsilon) * dx                       
        xsum = beta * xsum + (1-beta) * deltax**2
        x = x + deltax
        path.append(x)
        
        if (dx.dot(dx) < tol):
            break

methods.append(Adadelta.__name__)

#RMSprop
def Adam(func, x0, path =[], eta = 0.06, beta1 = 0.75, beta2 = 0.75,  epsilon=1e-8, 
         nIter = 200, tol = 5e-3):
    x = x0
    path.append(x0)
    
    m = np.zeros(x0.shape)
    v = np.zeros(x0.shape)
    
    for i in range(nIter):
        dx = grad(func, x)        
        m = beta1 * m + (1 - beta1) * dx
        v = beta2 * v + (1 - beta2) * dx**2
        
        mhat = m / (1-beta1)
        vhat = v / (1-beta2)
        x = x - eta * mhat /(np.sqrt(vhat) + epsilon)
    
        path.append(x)
        if (dx.dot(dx) < tol):
            break

methods.append(Adam.__name__)


tempath = defaultdict(list)

for method in methods:
    path_ = []
    globals()[method](lossfunc, x0, path_)
    tempath[method].append(path_)
    
paths = [np.array(tempath[method]).T for method in methods]


fig, ax = plt.subplots(figsize=(10, 6))
ax.contour(x, y, z, levels=np.logspace(0, 5, 35), norm=LogNorm(), cmap=plt.cm.jet)
ax.plot(*minima_, 'r*', markersize=20)

ax.set_xlim((xmin, xmax))
ax.set_ylim((ymin, ymax))

anim = TrajectoryAnimation(*paths, labels=methods, ax=ax)

ax.legend(loc='upper right')

plt.show()

#uncomment 'plt.show()' to save to gif
#anim.save('sgdimg.gif', writer='imagemagick', dpi=72)


