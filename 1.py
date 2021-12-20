import cv2
from matplotlib import pyplot as plt
img = cv2.imread("testpic/plastic_cover.bmp")
   # print(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
for i in range(gray_img.shape[0]):
    for j in  range(gray_img.shape[1]):
        if gray_img[i,j]<30:
            gray_img[i,j]=0
plt.imshow(gray_img)
plt.show()