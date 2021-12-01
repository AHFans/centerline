import cv2
import numpy as np


def main():

    # 1.导入图片
    img_src = cv2.imread("metal.bmp")

    # 2.灰度处理与二值化
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    ret, img_bin = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # 3.连通域分析
    contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_EXTERNAL,
                                                        cv2.CHAIN_APPROX_SIMPLE)

    # 4.制作掩膜图片
    img_mask = np.zeros(img_src.shape, np.uint8)
    cv2.drawContours(img_mask, contours, -1, (255, 255, 255), -1)

    # 5.执行与运算
    img_result = cv2.bitwise_and(img_src, img_mask)

    # 6.显示结果
    cv2.imwrite("img_src.bmp", img_src)
    cv2.imwrite("img_mask.bmp", img_mask)
    cv2.imwrite("img_result.bmp", img_result)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

