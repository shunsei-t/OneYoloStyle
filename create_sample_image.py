import merge_image
import numpy as np
import cv2
import os

if __name__ == "__main__":
    os.mkdir("dataset")
    # repeat x 10(sampe_backgournd) images are created
    repeat = 100
    # Image name
    target_name = "hachiware"
    fore_name = target_name + ".png"
    back_name = "sample_background/sample_background_"
    xlist = np.arange(start=100, stop=1820, step=1, dtype=np.uint32)
    ylist = np.arange(start=100, stop=980, step=1, dtype=np.uint32)
    zlist = np.arange(start=0.3, stop=2.0, step=0.1, dtype=np.float32)
    divSize = 3

    for si in range(1, 11):
        for i in range(1, repeat+1):
            img, corners = merge_image.merge_image(fore_name,
                                                   back_name + str(si) + ".jpeg",
                                                   np.random.choice(xlist),
                                                   np.random.choice(ylist),
                                                   np.random.choice(360),
                                                   np.random.choice(zlist),
                                                   divSize)

            cnvCorners = np.array(corners, dtype=np.float32)
            cnvCorners[:, 0] /= img.shape[1]
            cnvCorners[:, 1] /= img.shape[0]
            cnvCorners = cnvCorners.reshape(cnvCorners.size)

            img_header = "dataset/" + target_name + "_" + str(si) + "_" + str(i)
            with open(img_header + ".txt", mode="w") as f:
                print(0, end=" ", file=f)
                print(*cnvCorners, sep=' ', file=f)

            cv2.imwrite(img_header + ".png", img)
            print("imwrite", img_header + ".png")
