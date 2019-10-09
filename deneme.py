'''
Created on Oct 9, 2019

@author: user
'''

import numpy as np
import matplotlib.pyplot as plt

def div(v):
    ret=np.zeros(v[0].shape)
    ret += np.gradient(v[0], axis=0)
    ret += np.gradient(v[1], axis=1)
    return ret
a=np.arange(4).reshape(2,2)
print(div(np.gradient(a)))