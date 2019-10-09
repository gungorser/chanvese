'''
Created on Oct 9, 2019

@author: user
'''
import matplotlib.pyplot as plt
from utils import lipschitz, hside

def image(path):
    ret = plt.imread(path)
    if ret.ndim==3:
        ret=ret[:,:,0]
        return ret
    
class Frontend():
    iter=0
    algorithms=[]
    def __init__(self, path, algorithms):
        self.figure = plt.figure()
        self.figure.subplots_adjust(hspace=.5)
        for i, algorithm in enumerate(algorithms):
            u=image(path)
            phi=lipschitz(8, u.shape)
            algorithm.__dict__.update({'u':u,'phi':phi})
            ax = plt.subplot(len(algorithms), 1, i+1, title=str(algorithm))
            h = ax.imshow(hside(phi))
            self.algorithms.append({'alg': algorithm, 'ax': ax, 'h': h })
            
    def update(self):
        while True:
            self.iter+=1
            self.figure.suptitle('{}. iteration'.format(self.iter))
            for algorithm in self.algorithms:
                algorithm['alg'].step()
                algorithm['h'].set_data(hside(algorithm['alg'].phi))
            plt.draw()
            plt.pause(1e-2)

