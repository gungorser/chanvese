'''
Created on Oct 9, 2019

@author: user
'''
from frontend import Frontend

if __name__ == '__main__':
    print('Running. Press CTRL-C to exit.')
    try:
        Frontend({
            'phi':{'mode':'uniform', 'radius': 10},
            'image':{'path': 'resource/crack.bmp'},
            'algorithms':[
                {'name':'ChanVese', 'kwargs':{'dt':.5, 'mu':0.2, 'v':0, 'lambda1':5, 'lambda2':5}}
                ,{'name':'ChanVese', 'kwargs':{'dt':.5, 'mu':0.8, 'v':0, 'lambda1':1, 'lambda2':1}}
            ]
        }).update()
    except KeyboardInterrupt:
        print('exiting...')