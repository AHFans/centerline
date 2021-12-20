import copy

import cv2
from matplotlib import pyplot as plt
from numpy import zeros, ones
'''
程序用来提取图像连通域的数量
'''

class Stack:
    """堆栈结构类"""
    def __init__(self):
        self._item = []

    def push(self, item):
        """
        添加新元素
        :param item:
        :return:
        """
        self._item.append(item)

    @property
    def size(self):
        """
        返回堆栈大小
        :return:
        """
        return len(self._item)

    @property
    def is_empty(self):
        """
        判断是否为空
        :return:
        """
        return  not self._item

    def pop(self):
        """
        弹出栈顶元素
        :return:
        """
        return self._item.pop()

    def peek(self):
        """
        返回栈顶元素
        :return:
        """
        return self._item[-1]
# class my_area:
#     def __init__(self):



def bwLabel(src,dst,RGB_PIC):
    rows=src.shape[0]
    print(rows)
    cols=src.shape[1]
    stack = Stack()
    labelvalue=0
    point_seed=[]
    area=0
    num_of_connect_domain = 0
    for i in range(rows):
        #pRow=dst[i]#取行
      #  print (i)
        #
        # print(pRow)
        for j in range(cols):
           # pRow = dst[i]

            if dst[i,j]==255:
                area=0
                labelvalue+=1
                seed=(i,j)
                dst[seed]=labelvalue
                stack.push(seed)
                area+=1
                coordinate=[]
                while stack.is_empty==0:
                   # print('fas')
                    if (seed[0]+1<rows):
                        neighbor=(seed[0]+1,seed[1])

                        if(seed[0]!=(rows-1))&(dst[neighbor]==255):
                            #print('s')
                            dst[neighbor]=labelvalue
                            #pRow = dst[i]
                            stack.push(neighbor)
                            coordinate.append(neighbor)
                            area+=1

                    if (seed[1] + 1 < cols):
                        neighbor=(seed[0],seed[1]+1)
                        if(seed[1]!=(cols-1))&(dst[neighbor]==255):
                            dst[neighbor] = labelvalue
                           # pRow = dst[i]


                            stack.push(neighbor)
                            coordinate.append(neighbor)
                            area += 1
                   # if(seed[0])
                    neighbor = (seed[0]-1, seed[1])
                    if (seed[0]!= 0) & (dst[neighbor] == 255):
                        dst[neighbor] = labelvalue
                       # pRow = dst[i]
                        stack.push(neighbor)
                        coordinate.append(neighbor)
                        area += 1
                    neighbor = (seed[0] , seed[1]-1)
                    if (seed[1] != 0) &(dst[neighbor] ==255):
                        dst[neighbor] = labelvalue
                      #  pRow = dst[i]
                        stack.push(neighbor)
                        coordinate.append(neighbor)
                        area += 1
                    seed=stack.peek()
                    stack.pop()
                if len(coordinate)>1000:
                    num_of_connect_domain+=1
                    for pix in range(0, len(coordinate)):
                         RGB_PIC= cv2.circle(RGB_PIC, (int(coordinate[pix][1]), int(coordinate[pix][0])), 1, (255, 0, 0), 1)
               # labelvalue += 1
    plt.imshow(RGB_PIC)
    plt.show()


    return num_of_connect_domain








if __name__ == '__main__':
    src1=cv2.imread("testpic/bowl2.bmp")
    gray_img = cv2.cvtColor(src1, cv2.COLOR_BGR2GRAY)
    print(gray_img.shape[0])
    print(gray_img.shape[1])
    tha, gray_img = cv2.threshold(gray_img, 230, 255, cv2.THRESH_BINARY)
    #dst=ones([gray_img.shape[0],gray_img.shape[1]])*255
    dst=copy.deepcopy(gray_img)

    num_of_connect_domain=bwLabel(gray_img,dst,src1)
    print('有',num_of_connect_domain,'个区域')