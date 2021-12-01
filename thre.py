import cv2
from matplotlib import pyplot as plt
def threshold(data):
    point=[]

    for x in range(0, data.shape[1]): # column
        max=0
        current=0
        for y in range(0, data.shape[0]): # line
             if data[y,x]>=data[max,x]:
                #print(data[x,y])
                max=y
        if data[max,x]>10:
            point.append((max,x))
    return point
if __name__=='__main__':
    img=cv2.imread("C:/Users/DELL/Desktop/2.jpg")
   # plt.subplot(1,2,1)
  #  plt.imshow(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   # img=cv2.GaussianBlur(img,[5,5],)
    pt=threshold(gray_img)
    for i in range(0,len(pt)):
        data = cv2.circle(img, (pt[i][1], pt[i][0]), 1, (255, 0, 0), 1)
 #   plt.subplot(1,2,2)
    plt.imshow(data)
    plt.show()