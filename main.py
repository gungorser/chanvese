'''
Created on Oct 9, 2019

@author: user
'''
from algorithm import ChanVese
from frontend import Frontend

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    try:
        Frontend({
            'phi':{'mode':'uniform', 'radius': 8},
            'image':{'path': 'resource/crack.jpg', 'inverse':False},
            'algorithms':[
                {'name':'ChanVese', 'kwargs':{'dt':1, 'mu':1, 'v':0, 'lambda1':1, 'lambda2':1}},
                {'name':'ChanVese2', 'kwargs':{'dt':1, 'mu':0, 'v':0, 'lambda1':1, 'lambda2':1}}
            ]
        }).update()
    except KeyboardInterrupt:
        print('exiting...')