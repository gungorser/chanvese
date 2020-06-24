import numpy as np
from utils import hside, dirac, avg_intensity, mean_curvature, divergent
        
class Algorithm():
    def __init__(self, phi, **kwargs):
        self.__dict__.update(kwargs)
        self.phi=np.copy(phi)
        self.dirac=dirac(self.phi)
        self.hside=hside(self.phi)
        
    def step(self):
        self.phi += self.increment_phi()
        self.dirac=dirac(self.phi)
        self.hside=hside(self.phi)
        
    def increment_phi(self):
        raise NotImplemented
    
    def correctphi(self):
        gradflux=np.gradient(self.phi)
        absgradflux=np.linalg.norm(gradflux, axis=0)
        self.phi += np.sign(self.phi)*(1-absgradflux)
    
class ChanVese(Algorithm):  
    def increment_phi(self):
        gradphi=np.gradient(self.phi)
        absgradphi=np.linalg.norm(gradphi, axis=0)
        length=self.mu*divergent(gradphi/(absgradphi+1e-10))
        c1, c2=avg_intensity(self.u, self.hside)
        return self.dt*self.dirac*(
            + length*mean_curvature(self.phi)
            - self.v
            - self.lambda1*(self.u-c1)**2 
            + self.lambda2*(self.u-c2)**2
        )
        
        
