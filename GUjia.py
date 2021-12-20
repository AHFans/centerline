import cv2
import numpy as np
def cv_show(img):
    cv2.imwrite('erosion.bmp', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
# 读取图片
image = cv2.imread("f.bmp", cv2.IMREAD_GRAYSCALE)
#gray_image =cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
print(image)
for i in range(image.shape[0]):
    for j in range (image.shape[1]):
        if image[i,j]>0:
            image[i,j]=255
kernel = np.ones((5, 5), dtype=np.uint8)
erosion = cv2.erode(image, kernel, iterations=1)
ss = np.hstack((image, erosion))
cv_show(ss)

