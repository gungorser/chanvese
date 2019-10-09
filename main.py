'''
Created on Oct 9, 2019

@author: user
'''
from algorithm import ChanVese, ChanVese2
from frontend import Frontend

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    try:
        Frontend(path='resource/crack.jpg',
            algorithms=[
            ChanVese2(mu=0, v=0, lambda1=1, lambda2=1),
            ChanVese(dt=1, mu=0, v=0, lambda1=1, lambda2=1),
        ]).update()
    except KeyboardInterrupt:
        print('exiting...')