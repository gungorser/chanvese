'''
Created on Oct 9, 2019

@author: user
'''
import numpy as np
import matplotlib.pyplot as plt

def lipschitz(radius, shape):
    x,y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    return radius - np.sqrt((x%(radius*4)-radius*2)**2 + (y%(radius*4)-radius*2)**2 )

def divergent(v):
    ret=np.zeros(v[0].shape)
    ret += np.gradient(v[0], axis=0)
    ret += np.gradient(v[1], axis=1)
    return ret

def dirac(x, ep=1):
    return ep/(np.pi*(ep**2+x**2))

def hside(x, ep=1):
    return (1+ (2*np.arctan(x/ep))/np.pi)/2

class Diff():
    def __init__(self, x):
        self.cnt = np.pad(x, 2, mode='edge')
        self.C1=1/np.sqrt(0.000000001+(self(1,0)-self(0,0))**2 + (self(0,1)-self(0,-1))**2/4)
        self.C2=1/np.sqrt(0.000000001+(self(0,0)-self(-1,0))**2 + (self(-1,0)-self(-1,-1))**2/4)
        self.C3=1/np.sqrt(0.000000001+(self(1,0)-self(-1,0))**2/4 + (self(0,1)-self(0,0))**2)
        self.C4=1/np.sqrt(0.000000001+(self(1,-1)-self(-1,-1))**2/4 + (self(0,0)-self(0,-1))**2)
        
    def __call__(self, i, j):
        return self.cnt[2+i:-2+i, 2+j:-2+j]
    
def avg_intensity(u, hside):
    ihside = 1-hside
    c1=np.sum(u*hside)/np.sum(hside)
    c2=np.sum(u*ihside)/np.sum(ihside)
    return c1, c2
        
        
        
        
        