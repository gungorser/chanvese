import numpy as np
from utils import hside, dirac, avg_intensity, Diff, divergent
        
class Algorithm():
    def step(self):
        raise NotImplemented
    
    def draw(self):
        raise NotImplemented
    
class ChanVese(Algorithm):
    def __init__(self, u, phi, dt, mu, v, lambda1, lambda2):
        self.u=u
        self.phi=phi
        self.dt=dt
        self.mu=mu
        self.v=v
        self.lambda1=lambda1
        self.lambda2=lambda2
        self.dirac=dirac(self.phi)
        self.hside=hside(self.phi)
        
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
            
    def draw(self):
        return {
            'phi': self.phi,
            'hside': self.hside,
            'dirac': self.dirac,
        }
    
    def correctphi(self):
        gradflux=np.gradient(self.phi)
        absgradflux=np.linalg.norm(gradflux, axis=0)
        self.phi += np.sign(self.phi)*(1-absgradflux)
    
    def __str__(self):
        return 'mu:{}, v:{}, lambda1:{}, lambda2:{}'.format(self.mu, self.v, self.lambda1, self.lambda2)

class ChanVese2(Algorithm):
    def __init__(self, mu, v, lambda1, lambda2):
            self.mu=mu
            self.v=v
            self.lambda1=lambda1
            self.lambda2=lambda2
    
    def step(self):
        diracphi=dirac(self.phi)
        hsidephi=hside(self.phi)
        gradphi=np.gradient(self.phi)
        absgradphi=np.linalg.norm(gradphi, axis=0)
        div=self.k()
        c1, c2=avg_intensity(self.u, hsidephi)
        length=np.sum(diracphi*absgradphi)
        deltaphi=diracphi*(self.mu*length*div-self.v-self.lambda1*(self.u-c1)**2+self.lambda2*(self.u-c2)**2)
        self.phi+=deltaphi
    
    def k(self):
        dx=np.gradient(self.phi, axis=1)
        dy=np.gradient(self.phi, axis=0)
        dxx=np.gradient(dx, axis=1)
        dyy=np.gradient(dy, axis=0)
        dxy=np.gradient(dx, axis=0)
        return (dxx*dy**2-2*dxy*dx*dy+dyy*dx**2)/(dx**2+dy**2)**(3/2)
    
    def __str__(self):
        return 'mu:{}, v:{}, lambda1:{}, lambda2:{}'.format(self.mu, self.v, self.lambda1, self.lambda2)
        

    
    
