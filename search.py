import cv2
from matplotlib import pyplot as plt
import math
from numpy import zeros

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

    def ex_thresh(self,row,col,thresh):
        if self.gray_img[row-1][col] or self.gray_img[row+1,col] or self.gray_img[row,col-1] or self.gray_img[row,col+1] or self.gray_img[row-1,col-1] or self.gray_img[row+1,col-1] or self.gray_img[row-1,col+1] or self.gray_img[row+1][col+1]
            return True
    def down(self):

    def search(self):
        for col in range(self.gray_img.shape[1]):
            for row in range(self.gray_img.shape[0]):
                if self.gray_img[row][col]>self.thresh:
                    if self.ex_thresh(row,col,self.thresh):
                        down()



