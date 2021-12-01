import cv2
from matplotlib import pyplot as plt
import math
from numpy import zeros
'''
采用极大值法提取中心线
在低噪声情况下效果好
'''
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
@timer
def maximum():

    img = cv2.imread("metal.bmp")
       # print(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray_img[1,1])
    thresh=100
    gray_img = cv2.GaussianBlur(gray_img, ksize=(0, 0), sigmaX=5, sigmaY=5)
    for x in range(0,gray_img.shape[0]):
        for y in range(0,gray_img.shape[1]):
            if gray_img[x, y]<thresh:
                gray_img[x,y]=0
    point=[]
    for i in range(gray_img.shape[0]):
        max=0
        for j in range(gray_img.shape[1]):
            if(gray_img[i,max]<gray_img[i,j]):
                max=j
        point.append((i,max))
    for i in range(0, len(point)):
        img_after_extraction = cv2.circle(img, (int(point[i][1]), int(point[i][0])), 1, (255, 0, 0), 1)
        cv2.imwrite('maximum.bmp',img_after_extraction)
    plt.imshow(img)
    plt.show()
if __name__=='__main__':
    maximum()


