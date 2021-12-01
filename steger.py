#
import numpy as np
import cv2
from matplotlib import pyplot as plt
def timer(func):
    def func_wrapper(*args,**kwargs):
        from time import time
        time_start = time()
        result = func(*args,**kwargs)
        time_end = time()
        time_spend = time_end - time_start
        print('\n{0} cost time {1} s\n'.format(func.__name__, time_spend))
        return result
    return func_wrapper
#Build a class named steger to get the center line extracted by steger algorithm
class steger:
    def __init__(self, img,sigmaX,sigmaY):
        self.img=img
        self.sigmax=sigmaX
        self.sigmay=sigmaY
    def computeDerivative(self):
        # blurr the image
        self.img = cv2.GaussianBlur(self.img, ksize=(0,0), sigmaX=self.sigmax, sigmaY=self.sigmay)
        # create filter for derivative calulation
        dxFilter = np.array([[1],[-1]])
        dyFilter = np.array([[1,-1]])
        dxxFilter = np.array([[1],[-2],[1]])
        dyyFilter = np.array([[1,-2,1]])
        dxyFilter = np.array([[1,-1],[-1,1]])
        # compute derivative
        dx = cv2.filter2D(self.img,-1, dxFilter)
        dy = cv2.filter2D(self.img,-1, dyFilter)
        dxx = cv2.filter2D(self.img,-1, dxxFilter)
        dyy = cv2.filter2D(self.img,-1, dyyFilter)
        dxy = cv2.filter2D(self.img,-1, dxyFilter)
        return dx, dy, dxx, dyy, dxy
    def computeMagnitude(self,dxx, dyy):
        # convert to float
        dxx = dxx.astype(float)
        dyy = dyy.astype(float)
        # calculate magnitude and angle
        mag = cv2.magnitude(dxx, dyy)
        phase = mag*180./np.pi
        return mag, phase

    def computeHessian(self,dx, dy, dxx, dyy, dxy):
        # create empty list
        point=[]
        direction=[]
        value=[]
        # for the all image
        for x in range(0, img.shape[1]): # column
            for y in range(0, img.shape[0]): # line
                # if superior to certain threshold
                if gray_img[y,x]>180:#对于灰度大于100才计算

                  if dxy[y,x] > 0:
                    # compute local hessian
                     hessian = np.zeros((2,2))
                     hessian[0,0] = dxx[y,x]
                     hessian[0,1] = dxy[y,x]
                     hessian[1,0] = dxy[y,x]
                     hessian[1,1] = dyy[y,x]
                    # compute eigen vector and eigne value
                     ret, eigenVal, eigenVect = cv2.eigen(hessian)
                     if np.abs(eigenVal[0,0]) >= np.abs(eigenVal[1,0]):
                        nx = eigenVect[0,0]
                        ny = eigenVect[0,1]
                     else:
                        nx = eigenVect[1,0]
                        ny = eigenVect[1,1]
                    # calculate denominator for the taylor polynomial expension
                     denom = dxx[y,x]*nx*nx + dyy[y,x]*ny*ny + 2*dxy[y,x]*nx*ny
                    # verify non zero denom
                     if denom != 0:
                        T = -(dx[y,x]*nx + dy[y,x]*ny)/denom
                        # update point
                        if np.abs(T*nx) <= 0.5 and np.abs(T*ny) <= 0.5:
                            point.append((x,y))
                            direction.append((nx,ny))
                            value.append(np.abs(dxy[y,x]+dxy[y,x]))
        return point, direction, value
    @timer
    def drawimg(self):
        dx, dy, dxx, dyy, dxy = self.computeDerivative()
       # normal, phase = self.computeMagnitude(dxx, dyy)
        pt, dir, val = self.computeHessian(dx, dy, dxx, dyy, dxy)
        for i in range(0, len(pt)):
            self.img = cv2.circle(img, (pt[i][0], pt[i][1]), 1, (255, 0, 0), 1)

        plt.imshow(self.img)
        plt.show()
# resize, grayscale and blurr
img = cv2.imread("bowl2.bmp")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#img = cv2.resize(img, (640,480))
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
stegerimg=steger(gray_img,6, 6)
stegerimg.drawimg()
