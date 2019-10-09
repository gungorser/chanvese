import numpy as np
import matplotlib.pyplot as plt
from signal import signal, SIGINT
from sys import exit

def lipschitz(radius, shape):
    x,y = np.meshgrid(np.arange(shape[1]), np.arange(shape[0]))
    return radius - np.sqrt((x%(radius*4)-radius*2)**2 + (y%(radius*4)-radius*2)**2 )

class diff():
    def __init__(self, x):
        self.cnt = np.pad(x, 2, mode='edge')
        self.C1=1/np.sqrt(0.000000001+(self(1,0)-self(0,0))**2 + (self(0,1)-self(0,-1))**2/4)
        self.C2=1/np.sqrt(0.000000001+(self(0,0)-self(-1,0))**2 + (self(-1,0)-self(-1,-1))**2/4)
        self.C3=1/np.sqrt(0.000000001+(self(1,0)-self(-1,0))**2/4 + (self(0,1)-self(0,0))**2)
        self.C4=1/np.sqrt(0.000000001+(self(1,-1)-self(-1,-1))**2/4 + (self(0,0)-self(0,-1))**2)
        
    def __call__(self, i, j):
        return self.cnt[2+i:-2+i, 2+j:-2+j]
    
def dirac(x, ep=1):
    return ep/(np.pi*(ep**2+x**2))

def hside(x, ep=1):
    return (1+ (2*np.arctan(x/ep))/np.pi)/2

def image(path):
    ret = plt.imread(path)
    if ret.ndim==3:
        ret=ret[:,:,0]
        return ret

class AverageIntensity():
    def __init__(self, u, hside):
        self.u = u
        self.hside = hside
        self.ihside = 1-self.hside
        self.c1=np.sum(self.u*self.hside)/np.sum(self.hside)
        self.c2=np.sum(self.u*self.ihside)/np.sum(self.ihside)

class Frontend():
    def __init__(self, alg, path):
        self.alg=alg
        self.iter=0
        self.fg, self.ax = plt.subplots(len(alg))
        self.fg.subplots_adjust(hspace=.5)
        self.h=[]
        for i, ax in enumerate(self.ax):
            alg[i].u=image(path)
            alg[i].phi=lipschitz(8, alg[i].u.shape)
            ax.set_title(str(alg[i]))
            self.h.append(ax.imshow(hside(alg[i].phi)))
            
    def update(self):
        self.iter+=1
        self.fg.suptitle('{}. iteration'.format(self.iter))
        for i, alg in enumerate(self.alg):
            alg.step()
            self.h[i].set_data(hside(alg.phi))
        plt.draw()
        plt.pause(1e-2)
        
class Algorithm():
    def step(self):
        pass
    
class ChanVese(Algorithm):
    def __init__(self, mu, v, lambda1, lambda2):
        Algorithm.__init__(self)
        self.mu=mu
        self.v=v
        self.lambda1=lambda1
        self.lambda2=lambda2
        
    def step(self):
        dphi=dirac(self.phi)
        hphi=hside(self.phi)
        len=np.sum(dphi*np.linalg.norm(np.gradient(self.phi), axis=0))
        tmp1=self.mu*dphi*len*0.01
        df = diff(self.phi)
        ai = AverageIntensity(self.u, hphi)
        self.phi=( self.phi
            + tmp1*(df.C1*df(1,0)+df.C2*df(-1,0)+df.C3*df(0,1)+df.C4*df(0,-1))
            - 0.01*dphi*(self.v + self.lambda1*(self.u-ai.c1)**2 - self.lambda2*(self.u-ai.c2)**2)) / ( 1 + tmp1*(df.C1+df.C2+df.C3+df.C4) )
    
    def __str__(self):
        return 'mu:{}, v:{}, lambda1:{}, lambda2:{}'.format(self.mu, self.v, self.lambda1, self.lambda2)

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    fe=Frontend([
        ChanVese(1,  0,   1,  1),
        ChanVese(0,   0,   1,  1)]
    , 'resource/crack.jpg')
    try:
        while True:
            fe.update()
    except KeyboardInterrupt:
        print('exiting...')
    
    
