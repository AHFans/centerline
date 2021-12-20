import cv2
from matplotlib import pyplot as plt
import math
from numpy import zeros
import sys

sys.setrecursionlimit(100000)  # 例如这里设置为十万


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
class searcher:
    def __init__(self,gray_img,thresh):
        self.gray_img=gray_img
        self.thresh=thresh
        self.point=[]
        self.edgepoint=[]
        self.search_point=(0,0)#搜索点初始化
        self.col=0
        self.maxcol=0
       # self.search_outline()
        self.preprocessing()
        self.state = 7
        self.next_state = 7
        self.col = []
        self.next_col=0
        self.num_of_area=0
        self.search()
        self.drawing()


    def preprocessing(self):
        self.gray_img = cv2.GaussianBlur(self.gray_img, ksize=(0, 0), sigmaX=5, sigmaY=5)
        #   retval,img_global=cv2.threshold(self.grayimg ,130,255,cv2.THRESH_BINARY)
        # for x in range(0, self.gray_img.shape[0]):  # column
        #     for y in range(0, self.gray_img.shape[1]):  # line
        #         if self.gray_img[x, y] < 200:
        #             self.gray_img[x, y] = 0
        # cv2.imwrite('f.bmp', self.gray_img)
    # def search7(self,row,col):
    #
    #
    #         self.down(row - 1, col + 1)
    #         self.ex_thresh(row - 1, col + 1)
    # def search0(self,row,col):
    #        #     self.edgepoint.append((row,col+1))
    #
    #             self.down(row, col + 1)
    #             self.ex_thresh(row, col + 1)
    # def search1(self,row,col):
    #       #  self.edgepoint.append((row + 1, col + 1))
    #
    #         self.down(row + 1, col + 1)
    #         self.ex_thresh(row + 1, col + 1)
    # def search2(self,row,col):
    #       #  self.edgepoint.append((row + 1, col))
    #         self.down(row + 1, col)
    #         self.ex_thresh(row + 1, col)
    # def search3(self,row,col):
    #       #  self.edgepoint.append((row + 1, col-1))
    #         self.down(row + 1, col-1)
    #         self.ex_thresh(row + 1, col-1)
    # def search4(self,row,col):
    #      #   self.edgepoint.append((row , col-1))
    #         self.down(row , col-1)
    #         self.ex_thresh(row , col-1)
    # def search5(self,row,col):
    #        # self.edgepoint.append((row-1 , col-1))
    #         self.down(row-1 , col-1)
    #         self.ex_thresh(row-1 , col-1)
    # def search6(self,row,col):
    #     #self.edgepoint.append((row - 1, col))
    #     self.down(row - 1, col)
    #     self.ex_thresh(row-1, col)
    def ex_thresh(self):
        '''

        :param row:
        :param col:
        :param thresh:
        :return:

        '''
        row=self.search_point[0]
        col=self.search_point[1]
        print(self.search_point)
        if (row+1)<gray_img.shape[0]&(col+1)<gray_img.shape[1]:
            if self.gray_img[row - 1, col + 1] > self.thresh: #7
                if(row-1,col+1) not in self.edgepoint:
                        #print(row,col)
                        self.edgepoint.append((row - 1, col + 1))
                      #  self.next_state = 5
                        self.down(row - 1, col + 1)
                        self.search_point=(row-1,col-1)
                        self.ex_thresh()

                else:
                        return True
            elif self.gray_img[row,col+1]>self.thresh:
                if (row, col + 1) not in self.edgepoint: #0
                     #   print(row, col)
                        self.edgepoint.append((row , col + 1))
                      #  self.next_state = 7
                        self.down(row, col + 1)
                        self.search_point = (row, col+1)
                        self.ex_thresh()

                else:
                        #self.col = col + 1
                      #  self.next_state = 7
                        return True
            elif self.gray_img[row + 1, col + 1] > self.thresh: #1
                if (row+1, col + 1) not in self.edgepoint:
                     #   print(row, col)
                        self.edgepoint.append((row +1, col + 1))
                       # self.next_state = 7
                        self.down(row + 1, col + 1)
                        self.search_point = (row + 1, col +1)
                        self.ex_thresh()

                else:
                      #  self.col = col + 1
                        self.next_state = 7.
                        return True
            elif self.gray_img[row + 1, col] > self.thresh:#2
                if (row+1, col ) not in self.edgepoint:
                      #  print(row, col)
                        self.edgepoint.append((row+1 , col))
                        self.down(row + 1, col )
                        self.search_point = (row + 1, col )
                        self.ex_thresh()
                      #  self.next_state = 1
                      #  self.search2(row,col)

                else:
                      #  self.col = col + 1
                     #   self.next_state = 7

                        return True

            else:
                    self.next_col=col+1

                    return False


    def down(self,row,col):
        #在down之前先判断该列重心是否已经被计算
     if col not in self.col:
          #  print('down',row,col)
            num = 0
            sum = 0
            for j in range (row,self.gray_img.shape[0]-1):
                  print(j,col)

                # print(self.gray_img.shape[0])
                # print(self.gray_img.shape[1])
                  if(self.gray_img[j,col]>=self.thresh):
                    #  self.point.append((j, col))
                      num+=self.gray_img[j,col]
                      sum+=self.gray_img[j,col]*j
                  else :
                      break
            self.point.append((int(sum/num),col))
            self.col.append(col)


    def search(self):
       # pointcol = []
        col=0
        while col<self.gray_img.shape[1]-1: #对列遍历
        #    print(col)
            for row in range(self.gray_img.shape[0]-1):#对行遍历
               # print(row, col)
                if self.gray_img[row,col]>self.thresh: #如果大于阈值，就记录该点为跟踪起始点
                  #  print(row,col)
                    self.search_point=(row,col)
                    print(self.search_point)
                    if self.ex_thresh()==False:
                      print(self.next_col)
                      col=self.next_col
                      break
            col+=1

            self.num_of_area += 1
        print('有',self.num_of_area,'个区域')
                    #col = self.col
                  # ==False:#判断周围是否有点，若无则证明是孤立点
                  #      self.gray_img[row,col]=0


                     #   print('ys')
                       # self.down(row,col)
                    #否则认为是噪声点
                    #self.search_outline(row,col)

                  #  col=self.maxcol+1

    def drawing(self):
        global img
        for i in range(len(self.point)):
            imga=cv2.circle(img, (int(self.point[i][1]), int(self.point[i][0])), 1, (255, 0, 0), 1)
        plt.imshow(imga)
        plt.show()

if __name__=='__main__':





    global img
    img=cv2.imread("testpic/bowl2.bmp")
   # print(img)
  #  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dr=searcher(gray_img,200)
    #print("有",)



