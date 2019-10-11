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
            'phi':{'mode':'circles', 'circles': [{'radius':20, 'x':64, 'y':64}]},
            'image':{'path': 'resource/cluster.bmp', 'inverse':False},
            'algorithms':[
                {'name':'ChanVese2', 'kwargs':{'dt':100, 'mu':.8, 'v':-.3, 'lambda1':1, 'lambda2':1}},
                # {'name':'Ipachi', 'kwargs':{'dt':1, 'mu1':0, 'mu2':0, 'lambdaV1':1, 'lambdaV2':1, 'lambdaI1':1, 'lambdaI2':1}}
            ]
        }).update()
    except KeyboardInterrupt:
        print('exiting...')