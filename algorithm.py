import numpy as np
from utils import hside, dirac, avg_intensity, Diff, divergent
        
class Algorithm():
    def __init__(self, phi, u, **kwargs):
        self.phi=phi
        self.u=u/np.max(u)
        self.__dict__.update(kwargs)
        self.dirac=dirac(self.phi)
        self.hside=hside(self.phi)
        
    def step(self):
        self.phi += self.increment_phi()
        self.dirac=dirac(self.phi)
        self.hside=hside(self.phi)
        
    def increment_phi(self):
        raise NotImplemented
    
    def draw(self):
        return {
            'hside': self.hside,
            'phi': self.phi,
            'dirac': self.dirac,
        }
        
    def correctphi(self):
        gradflux=np.gradient(self.phi)
        absgradflux=np.linalg.norm(gradflux, axis=0)
        self.phi += np.sign(self.phi)*(1-absgradflux)
         
class ChanVese(Algorithm):
    def step(self):
        length=np.sum(self.dirac*np.linalg.norm(np.gradient(self.phi), axis=0))
        tmp1=self.dt*self.dirac*self.mu*length
        df = Diff(self.phi)
        c1, c2=avg_intensity(self.u, self.hside)
        self.phi=( self.phi
            + tmp1*(df.C1*df(1,0)+df.C2*df(-1,0)+df.C3*df(0,1)+df.C4*df(0,-1))
            - self.dt*self.dirac*(self.v + self.lambda1*(self.u-c1)**2 - self.lambda2*(self.u-c2)**2)) \
            / ( 1 + tmp1*(df.C1+df.C2+df.C3+df.C4) )
        self.dirac=dirac(self.phi)
        self.hside=hside(self.phi)
    
class ChanVese2(Algorithm):  
    def increment_phi(self):
        gradphi=np.gradient(self.phi)
        absgradphi=np.linalg.norm(gradphi, axis=0)
        length=self.mu*divergent(gradphi/(absgradphi+1e-10))
        c1, c2=avg_intensity(self.u, self.hside)
        return self.dt*self.dirac*(
            + length
            - self.v
            - self.lambda1*(self.u-c1)**2 
            + self.lambda2*(self.u-c2)**2
        )
        
class Ipachi(Algorithm):
    def increment_phi(self):
        self.LP=np.fft.fft(self.phi)
        g=1/(1+np.imag(self.LP))
        return 0

        
