import cv2
from matplotlib import pyplot as plt
import math
from numpy import zeros
import numpy as np
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
#此方法先用极值法得到中心点再用方向模板法展开计算高斯中心
@timer
class module:
    def __init__(self,grayimg,sigmax,sigmay,order):
        self.grayimg=grayimg #grayimg
      #  self.threshold=threshold
        self.sigmax=sigmax
        self.sigmay=sigmay
        self.order=order
        self.createmodule()
        self.preprocessing()
    def createmodule(self):
        #create Horizental_filter,Vertical_filter,Right_filter,Left_filter to match the stripe direction
        self.Horizental_filter=zeros([self.order,self.order]) #horizental
        self.Vertical_filter = zeros([self.order, self.order])#veritical
        self.Right_filter = zeros([self.order, self.order])#Tilt right 45 degrees
        self.Left_filter = zeros([self.order, self.order])#Tilt left 45 degrees
        self.Horizental_filter[math.floor(self.order/2),:]=1
        self.Vertical_filter[:,math.floor(self.order / 2)] = 1
        for i in range(self.order):
            for j in range(self.order):
                if i == j:
                    self.Right_filter[i, j] = 1
                if (i + j) == (self.order-1):
                    self.Left_filter[i, j] = 1
    def preprocessing(self):
        self.grayimg = cv2.GaussianBlur(self.grayimg, ksize=(0, 0), sigmaX=self.sigmax, sigmaY=self.sigmay)
     #   retval,img_global=cv2.threshold(self.grayimg ,130,255,cv2.THRESH_BINARY)
        for x in range(0, self.grayimg.shape[0]):  # column
            for y in range(0, self.grayimg.shape[1]):  # line
                if self.grayimg[x, y] < 230:
                    self.grayimg[x, y] = 0
        cv2.imwrite('f.bmp',self.grayimg)
    def calculate(self,row,col):
        for i in range(self.order):
            max_col=0
            sum_M1=0
            sum_M2=0
            sum_M3=0
            sum_M4=0
            for j in range(self.order):
                sum_M1+=self.Horizental_filter[row,j]*self.grayimg[row-self.order/2+i,col-self.order/2+j]
            return sum_M1
                #sum_M2 += self.Horizental_filter[row, j] * self.grayimg[row - self.order / 2 + i, col - self.order / 2 + j]
    def extraction(self):
        width=self.grayimg.shape[0]
        height=self.grayimg.shape[1]
        for i in range (width):
            max_point_col=
            max_point_value=0
            for j in range (height):
                sum_M1=self.calculate(i,j)
                if(sum_M1)>max_point_value:
                    max_point_value=sum_M1
                    max_point_col=j
    def drawing(self,img):
        for i in range(0, len(self.point)):
            img = cv2.circle(img, (int(self.point[i][0]), int(self.point[i][1])), 1, (255, 0, 0), 1)
        cv2.imwrite('safecap_extraction1.bmp', img)
        plt.imshow(img)
        plt.show()


if __name__=='__main__':

    img = cv2.imread("testpic/bowl2.bmp")
   # print(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dr=module(gray_img,2,2,10)
    dr.extraction()
    dr.drawing(img)





