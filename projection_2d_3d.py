# Project a point from 3D to 2D using a matrix operation

## Given a point in 3-space [x y z], and focal length f
## Return : Location of the projected point on 2D image plane [u v]

import numpy as np

def p_img (p,f):
    A = [[f , 0 , 0 , 0],
         [0, f, 0, 0],
         [0, 0, 1, 0]
         ]
    # Convert p to homogeneous coordinates and transpose (size: 4x1)
    p_hom = np.append(p,[1]).reshape(4,1)
    # examle:
        # [[200]
        #  [100]
        #  [50]
        #  [1]]

    print p_hom
    p_proj = np.dot(A ,p_hom)
    # RESULT example :
        # [[10000]
        #  [5000]
        #  [50]]
        #
    ## convert back to non-homogeneus coordinates and return
    p_img = [p_proj[0]/p_proj[2], p_proj[1]/p_proj[2]]
    return p_img
p = [200, 100, 50]
f = 50
print (p_img(p,f))
