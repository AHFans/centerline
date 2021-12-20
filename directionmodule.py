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
    def extraction(self):
        self.point = []
        self.skeleton_point = []
        #先用self.skeleton_point记录极大值法提取骨架的初始点
        for i in range(math.ceil(self.order/2), self.grayimg.shape[0] - math.ceil(self.order/2)):
            max1 = 0
            for j in range(math.ceil(self.order/2), self.grayimg.shape[1] - math.ceil(self.order/2)):
                if self.grayimg[i, j] >= self.grayimg[i, max1]:
                    max1 = j
            self.skeleton_point.append((i, max1))
        #创建Image_after_horizentalfilter,Image_after_leftfilter记录每个Point点的模板计算结果
        len_self_skeleton_point=len(self.skeleton_point)
        Image_after_horizentalfilter = zeros(len_self_skeleton_point)
        Image_after_verticalfilter = zeros(len_self_skeleton_point)
        Image_after_Rightfilter = zeros(len_self_skeleton_point)
        Image_after_leftfilter = zeros(len_self_skeleton_point)
        edge=math.ceil(self.order/2)


        for i in range(0, len(self.skeleton_point)):
            if self.grayimg[self.skeleton_point[i][0], self.skeleton_point[i][1]]:
                x_leftedge = self.skeleton_point[i][0] - edge
                y_leftedge = self.skeleton_point[i][1] - edge
                x_rightedge=self.skeleton_point[i][0] + edge
                for x in range(self.order):
                    for y in range(self.order):
                        if self.Horizental_filter[x, y] or self.Vertical_filter[x, y] or self.Right_filter[x, y] or self.Left_filter[x, y]:
                            Image_after_horizentalfilter[i] += self.grayimg[x_leftedge + x, y_leftedge  + y] * self.Horizental_filter[x, y]
                            Image_after_verticalfilter[i] += self.grayimg[x_leftedge + x, y_leftedge + y] * self.Vertical_filter[x, y]
                            Image_after_Rightfilter[i] += self.grayimg[x_leftedge+ x, y_leftedge  + y] * self.Right_filter[x, y]
                            Image_after_leftfilter[i] += self.grayimg[x_leftedge + x, y_leftedge + y] * self.Left_filter[x, y]
                            Stripe_direction= [Image_after_horizentalfilter[i], Image_after_verticalfilter[i], Image_after_Rightfilter[i], Image_after_leftfilter[i]]
                            direction= Stripe_direction.index(max(Stripe_direction))
                            #判断条纹的方向，利用灰度重心法计算中心点


                            if direction == 0:
                                num1 = 0
                                num2 = 0
                                for k in range(self.order):
                                    num1 +=self.grayimg[self.skeleton_point[i][0], y_leftedge + k] * (y_leftedge + k)
                                    num2 +=self.grayimg[self.skeleton_point[i][0], y_leftedge+ k]
                                # print(num1)
                                # print(num2)
                                self.point.append((num1 / num2, self.skeleton_point[i][0]))
                            elif direction == 1:
                                num1 = 0
                                num2 = 0
                                for k in range(self.order):
                                    num1 += self.grayimg[x_leftedge + k, self.skeleton_point[i][1]] * (x_leftedge + k)
                                    num2 += self.grayimg[x_leftedge + k, self.skeleton_point[i][1]]
                                self.point.append((self.skeleton_point[i][1], num1 / num2))
                            elif direction == 2:
                                num1 = 0
                                num2 = 0
                                for k in range(self.order):
                                    num1 += self.grayimg[x_rightedge - k, y_leftedge + k] * (y_leftedge + k)
                                    num2 += self.grayimg[x_rightedge - k, y_leftedge + k]
                                centeru = num1 / num2
                                num1 = 0
                                num2 = 0
                                for k in range(self.order):
                                    num1 += self.grayimg[x_rightedge - k, y_leftedge + k] * (x_rightedge- k)
                                    num2 += self.grayimg[x_rightedge - k, y_leftedge+ k]
                                centerv = num1 / num2
                                self.point.append((centeru, centerv))
                            elif direction == 3:
                                num1 = 0
                                num2 = 0
                                for k in range(self.order):
                                    num1 += self.grayimg[x_leftedge + k, y_leftedge + k] * (y_leftedge + k)
                                    num2 += self.grayimg[x_leftedge + k, y_leftedge + k]
                                centeru = num1 / num2
                                num1 = 0
                                num2 = 0
                                for k in range(self.order):
                                    num1 += self.grayimg[x_leftedge+ k, y_leftedge + k] * (x_leftedge + k)
                                    num2 += self.grayimg[x_leftedge + k, y_leftedge + k]
                                centerv = num1 / num2
                                self.point.append((centeru, centerv))
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




