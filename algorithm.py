import numpy as np
from utils import hside, dirac, avg_intensity, Diff, divergent
        
class Algorithm():
    def step(self):
        raise NotImplemented
    
class ChanVese(Algorithm):
    def __init__(self, dt, mu, v, lambda1, lambda2):
        self.dt=dt
        self.mu=mu
        self.v=v
        self.lambda1=lambda1
        self.lambda2=lambda2
        
    def step(self):
        dphi=dirac(self.phi)
        hphi=hside(self.phi)
        length=np.sum(dphi*np.linalg.norm(np.gradient(self.phi), axis=0))
        tmp1=self.mu*dphi*length*self.dt
        df = Diff(self.phi)
        c1, c2=avg_intensity(self.u, hphi)
        self.phi=( self.phi
            + tmp1*(df.C1*df(1,0)+df.C2*df(-1,0)+df.C3*df(0,1)+df.C4*df(0,-1))
            - self.dt*dphi*(self.v + self.lambda1*(self.u-c1)**2 - self.lambda2*(self.u-c2)**2)) / ( 1 + tmp1*(df.C1+df.C2+df.C3+df.C4) )
    
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
        div=divergent(gradphi/absgradphi)
        c1, c2=avg_intensity(self.u, hsidephi)
        len=np.sum(diracphi*absgradphi)
        deltaphi=diracphi*(self.mu*len*div-self.v-self.lambda1*(self.u-c1)**2+self.lambda2*(self.u-c2)**2)
        self.phi+=deltaphi
    
    def __str__(self):
        return 'mu:{}, v:{}, lambda1:{}, lambda2:{}'.format(self.mu, self.v, self.lambda1, self.lambda2)
        

    
    
