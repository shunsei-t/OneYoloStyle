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

    # 幾何変換行列の取得((回転中心), 角度, 拡大率)
    M = cv2.getRotationMatrix2D((foreH/2, foreW/2), dc, dz)

    M[0, -1] += int(dx - foreW/2)
    M[1, -1] += int(dy - foreH/2)

    # アフィン変換（変換後、空白の領域は透過率0が入るはず）
    img_warped = cv2.warpAffine(imgFore, M, (backW, backH))

    # 画像の重ね合わせ
    # img_warpedの透過率（[:, :, 3]）の比率で、imgBackとimg_warpedの画素値を配分する。（）
    # 例）imgBack[0, 0, 0] = imgBack[0, 0, 0]*(1-img_warped[0, 0, 3]/255) + img_warped[0, 0, 0]*(img_warped[1, 1, 3] / 255)
    # 例）           31.76 =               20*(1-                100/255) +                   0*(100/255)
    imgBack[:, :, 0] = imgBack[:, :, 0] * (1 - img_warped[:, :, 3] / 255) + img_warped[:, :, 0] * (img_warped[:, :, 3] / 255)
    imgBack[:, :, 1] = imgBack[:, :, 1] * (1 - img_warped[:, :, 3] / 255) + img_warped[:, :, 1] * (img_warped[:, :, 3] / 255)
    imgBack[:, :, 2] = imgBack[:, :, 2] * (1 - img_warped[:, :, 3] / 255) + img_warped[:, :, 2] * (img_warped[:, :, 3] / 255)

    # リサイズ
    imgResize = cv2.resize(imgBack, (int(backW/divSize), int(backH/divSize)))

    resizeH, resizeW = imgResize.shape[:2]

    # 幾何変換後のimgForeに対する、Bouding boxの四つ角の位置
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