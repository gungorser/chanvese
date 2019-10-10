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
            'phi':{'mode':'circles', 'circles':[{'radius': 100, 'x':600, 'y':300}]},
            'image':{'path': 'resource/crack.jpg', 'inverse':True},
            'algorithms':[
                {'name':'ChanVese', 'kwargs':{'dt':10, 'mu':0, 'v':1, 'lambda1':10, 'lambda2':10}}
            ]
        }).update()
    except KeyboardInterrupt:
        print('exiting...')