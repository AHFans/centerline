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
class graycore:
    '''
    类包含预处理和提取、画图三部分
    预处理采用高斯滤波，参数sigmax和sigmay可以调整
    提取采用先极大值法再灰度重心法
    '''
    def __init__(self,gray_img,sigmax,sigmay):
        self.gray_img=gray_img
        self.sigmax=sigmax
        self.sigmay=sigmay
        self.proprocessing()
        self.graycore()
        self.drawing()
    @timer
    def graycore(self):
        max_point=[]
        self.point=[]
        #print(self.gray_img)
        for x in range (0,self.gray_img.shape[0]):
            max_y=0
            for y in range(0,self.gray_img.shape[1]):
               if(gray_img[x,max_y]<=gray_img[x,y]):
                   max_y=y
            if(gray_img[x,max_y]>150):
                max_point.append((x,max_y))

        for i in range(len(max_point)):
            sum=0
            num=0
            for j in range (-5,6):
                sum+=(max_point[i][1]+j)*self.gray_img[max_point[i][0],max_point[i][1]+j]
                num+=self.gray_img[max_point[i][0],max_point[i][1]+j]
            self.point.append((max_point[i][0],int(sum/num)))

       # return point
    def proprocessing(self):
        self.gray_img=cv2.GaussianBlur(self.gray_img,ksize=(0, 0), sigmaX=self.sigmax, sigmaY=self.sigmay)
    def drawing(self):
        print(len(self.point))
        for i in range(0, len(self.point)):

            img_after_extract = cv2.circle(img, (self.point[i][1], self.point[i][0]), 1, (255, 0, 0), 1)
        cv2.imwrite('graycore_afer_extraction.bmp',img_after_extract)
        plt.imshow(img_after_extract)
        plt.show()

if __name__=='__main__':

    img = cv2.imread("bowl.bmp")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    pt=graycore(gray_img,6,6)

