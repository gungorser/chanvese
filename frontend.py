'''
Created on Oct 9, 2019

@author: user
'''
import matplotlib.pyplot as plt
from utils import lipschitz
import numpy as np

def readimage(path, LUT=None):
    ret = plt.imread(path)
    if ret.ndim==3:
        ret=ret[:,:,0]
    
    if LUT:
        t=np.zeros(256,dtype=np.uint8)
        t[LUT[0]:LUT[1]]=np.linspace(start=0,stop=255,num=LUT[1]-LUT[0],endpoint=True,dtype=np.uint8)
        ret=t[ret]
        
    return ret
    
class Frontend():
    iter=0
    algorithms=[]
    def __init__(self, config):
        self.figure = plt.figure()
        self.figure.subplots_adjust(hspace=.5)
        u=readimage(**(config['image']))
        phi=lipschitz(u.shape, **config['phi'])
        subplotsize_x=1
        if 'LUT' in config['image']:
            subplotsize_x=2
        subplotsize_x=max(subplotsize_x, len(config['algorithms']))
        subplotsize_y=1
        if len(config['algorithms'])>0:
            subplotsize_y=2
        
        for algorithmconf in config['algorithms']:
            module = __import__('algorithm')
            class_ = getattr(module, algorithmconf['name'])
            algorithmconf['kwargs'].update({'u':u, 'phi':phi})
            instance = class_(**algorithmconf['kwargs'])
            self.algorithms.append({'alg': instance})
        
        plt.subplot(subplotsize_y, subplotsize_x, 1, title='original image').imshow(plt.imread(config['image']['path']))
        if 'LUT' in config['image']:
            plt.subplot(subplotsize_y, subplotsize_x, 2, title='LUT applied').imshow(u, cmap='Greys')
            
        for i, algorithmconf in enumerate(config['algorithms']):
            algorithm=self.algorithms[i]
            ax=plt.subplot(subplotsize_y, subplotsize_x, subplotsize_x+i+1, 
                           title='dt:{dt} mu:{mu} v:{v} L1:{lambda1} L2:{lambda2}'.format(**algorithmconf['kwargs']))
            h=ax.imshow(algorithm['alg'].hside)
            algorithm['infos']={'ax': ax,'h': h}
        self.draw()
        
    def draw(self):
        self.figure.suptitle('{}. iteration'.format(self.iter))
        plt.draw()
        plt.pause(1e-2)
        self.iter+=1
            
    def update(self):
        while True:
            for algorithm in self.algorithms:
                algorithm['alg'].step()
                algorithm['infos']['h'].set_data(algorithm['alg'].hside)
            self.draw()

