import cv2
import numpy as np
import sys

def merge_image(imgForeName, imgBackName, dx, dy, dc, dz, divSize):
    """
    @param dx imgBackにおける横位置
    @param dy imgBackにおける縦位置
    @param dc [degree]回転量
    @param dz 拡大率
    @param divSize 出力画像のリサイズ
    """
    imgFore = cv2.imread(imgForeName, cv2.IMREAD_UNCHANGED)
    imgBack = cv2.imread(imgBackName)

    foreH, foreW = imgFore.shape[:2]
    backH, backW = imgBack.shape[:2]

    # ((回転中心), 角度, 拡大率)
    M = cv2.getRotationMatrix2D((foreH/2, foreW/2), dc, dz)

    M[0, -1] += int(dx - foreW/2)
    M[1, -1] += int(dy - foreH/2)

    img_warped = cv2.warpAffine(imgFore, M, (backW, backH))

    imgBack[:, :, 0] = imgBack[:, :, 0] * (1 - img_warped[:, :, 3] / 255) + img_warped[:, :, 0] * (img_warped[:, :, 3] / 255)
    imgBack[:, :, 1] = imgBack[:, :, 1] * (1 - img_warped[:, :, 3] / 255) + img_warped[:, :, 1] * (img_warped[:, :, 3] / 255)
    imgBack[:, :, 2] = imgBack[:, :, 2] * (1 - img_warped[:, :, 3] / 255) + img_warped[:, :, 2] * (img_warped[:, :, 3] / 255)

    imgResize = cv2.resize(imgBack, (int(backW/divSize), int(backH/divSize)))

    resizeH, resizeW = imgResize.shape[:2]

    rectCorners = [[int((dx - foreW*dz/2)/divSize), int((dy - foreH*dz/2)/divSize)],
                   [int((dx + foreW*dz/2)/divSize), int((dy - foreH*dz/2)/divSize)],
                   [int((dx + foreW*dz/2)/divSize), int((dy + foreH*dz/2)/divSize)],
                   [int((dx - foreW*dz/2)/divSize), int((dy + foreH*dz/2)/divSize)]]

    for corner in rectCorners:
        if corner[0] < 0:
            corner[0] = 0
        elif corner[0] > resizeW-1:
            corner[0] = resizeW-1
        if corner[1] < 0:
            corner[1] = 0
        elif corner[1] > resizeH-1:
            corner[1] = resizeH-1

    return imgResize, rectCorners

if __name__ == "__main__":
    fore_name = "./hachiware.png"
    back_name = "./sample_background/sample_background_1.jpeg"
    dx = 1500
    dy = 500
    dc = 0
    dz = 1.5
    divSize = 3

    img, corners = merge_image(fore_name, back_name, dx, dy, dc, dz, divSize)
    print(img.shape)
    print(corners)

    for corner in corners:
        img = cv2.circle(img, corner, 3, (0, 255, 255), thickness=-1, lineType=cv2.LINE_8, shift=0)

    cv2.imshow("img", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()