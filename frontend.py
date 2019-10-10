'''
Created on Oct 9, 2019

@author: user
'''
import matplotlib.pyplot as plt
from utils import lipschitz, hside

def readimage(path, inverse):
    ret = plt.imread(path)
    if ret.ndim==3:
        ret=ret[:,:,0]
    if inverse:
        ret=255-ret
    return ret
    
class Frontend():
    iter=0
    algorithms=[]
    def __init__(self, config):
        self.figure = plt.figure()
        self.figure.subplots_adjust(hspace=.5)
        u=readimage(**(config['image']))
        phi=lipschitz(u.shape, **config['phi'])
        subplotsize_x=0
        subplotsize_y=len(config['algorithms'])+1
        for algorithmconf in config['algorithms']:
            module = __import__('algorithm')
            class_ = getattr(module, algorithmconf['name'])
            algorithmconf['kwargs'].update({'u':u, 'phi':phi})
            instance = class_(**algorithmconf['kwargs'])
            self.algorithms.append({'alg': instance, 'infos':[]})
            subplotsize_x=max(subplotsize_x, len(instance.draw()))
        
        plt.subplot(subplotsize_y, subplotsize_x, 1, title='original image').imshow(u)
        for i, algorithmconf in enumerate(config['algorithms']):
            algorithm=self.algorithms[i]
            drawinfo=algorithm['alg'].draw()
            for j, drawinfo in enumerate(drawinfo.items()):
                ax=plt.subplot(subplotsize_y, subplotsize_x, subplotsize_x*(i+1)+j+1, title=drawinfo[0])
                h=ax.imshow(drawinfo[1])
                algorithm['infos'].append({'ax': ax,'h': h})
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
                drawinfos=algorithm['alg'].draw()
                for i, drawinfo in enumerate(drawinfos.items()):
                    algorithm['infos'][i]['h'].set_data(drawinfo[1])
            self.draw()

