# chanvese
chanvese algorithm


Compare Several Chan Vese session simultaneously, by applying different input parameters to the same image. 

##phi
The level set method, or initial phi. Giving an uniform phi will result faster.
  -uniform 
    radius
  -circles
    shape(x,y)

##image
Input image settings can be provided 
  -path
  -LUT[min,max]

##algorithms
Algorithm input parameters can be provided. Available Algorithms: Chan Vese only
  -name
  -kwargs
    dt, mu, v, lambda1, lambda2 (for chan vese only)
    
Usage:
{
    'phi':{'mode':'uniform', 'radius': 10},
    'image':{'path': 'resource/crack.bmp'},
    'algorithms':[
        {'name':'ChanVese', 'kwargs':{'dt':.5, 'mu':0.2, 'v':0, 'lambda1':5, 'lambda2':5}}
        ,{'name':'ChanVese', 'kwargs':{'dt':.5, 'mu':0.8, 'v':0, 'lambda1':1, 'lambda2':1}}
    ]
}
