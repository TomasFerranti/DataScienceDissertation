"""
split_image.py is a collection of functions to build an algorithm that automatically splits a stereo image in left, middle and right
"""
import cv2 as cv
import numpy as np
import sys


def getLogDist(array):
    """
    getLogDist creates a array of weights with shape of the input, where the earlier observations have more weight

    Parameters
    - array:np.array, numpy array of shape (n,)

    Return
    - weight:np.array, numpy array of shape (n,) and float values between [0, 1] * array
    """
    L = array.shape[0]
    X = np.arange(L)
    weight = array * (np.log(1 + L - X) / np.log(1 + L))
    return weight


def findBestAdds(img, c_x, c_y, r_x, r_y, image_left, ds=5):
    """
    findBestAdds expands the rectangle looking for the two segments of distance ds with the highest difference in RGB values

    Parameters
    - img:np.array, numpy array of shape (m,n,3)
    - c_x:int, coordinate x of center of rectangle
    - c_y:int, coordinate y of center of rectangle
    - r_x:list, list of two integers indicating the positive radius for left and right from center
    - r_y:list, list of two integers indicating the positive radius for up and down from center
    - image_left:bool, indicates if padding is needed (in case of right image)
    - ds:int, length of difference between segments

    Return
    - best_adds:list, four values to add to each radius (r_x[0], r_x[1], r_y[0], r_y[1]), respectively
    """
    # X axis padding necessary for right image
    x_padding = int(0.5*img.shape[1])
    if image_left:
        img = img[:, :-x_padding, :]
    else:
        x_padding -= 100
        img = img[:, x_padding:, :]
        c_x -= x_padding

    # Finding best adds for each rectangle side
    best_adds = []
    for coord in ['x', 'y']:
        for direction in ["minus", "plus"]:
            # Segs to test the best add based on for loop variables
            if coord == 'x':
                if direction == "minus":
                    segs = img[(c_y - r_y[0]): (c_y + r_y[1]),
                               0: (c_x - r_x[0])]
                else:
                    segs = img[(c_y - r_y[0]): (c_y + r_y[1]),
                               (c_x + r_x[1]): img.shape[1]]
            else:
                if direction == "minus":
                    segs = img[0: (c_y - r_y[0]),
                               (c_x - r_x[0]): (c_x + r_x[1])]
                else:
                    segs = img[(c_y + r_y[1]): img.shape[0],
                               (c_x - r_x[0]): (c_x + r_x[1])]
            if direction == "minus":
                segs = np.flip(segs)

            # Get best add
            segs = np.mean(segs, axis=int(coord == 'y'))
            segs_diff = np.sum(np.abs(segs[ds:] - segs[:-ds]), axis=1)
            segs_diff = getLogDist(segs_diff)
            best_add = ds + np.argmax(segs_diff)
            best_adds.append(best_add)
    return best_adds


def getStereoSplit(img):
    """
    getStereoSplit splits an img into three pieces (left, middle, right) using a deterministic heuristic

    Parameters
    - img:np.array, numpy array of shape (m,n,3)

    Return
    - imgL:np.array, numpy array of shape (mS,nS,3)
    - imgR:np.array, numpy array of shape (mS,nS,3)
    - imgM:np.array, numpy array of shape (mM,nM,3)
    """
    # Initial centers and radius of images left and right
    imgL_c_x = int(1/4 * img.shape[1])
    imgR_c_x = int(3/4 * img.shape[1])
    imgL_c_y = int(1/2 * img.shape[0])
    imgR_c_y = int(1/2 * img.shape[0])
    imgL_r_x = 2*[int((1/2 * 0.25) * img.shape[1])]
    imgR_r_x = 2*[int((1/2 * 0.25) * img.shape[1])]
    imgL_r_y = 2*[int((1/2 * 0.7) * img.shape[0])]
    imgR_r_y = 2*[int((1/2 * 0.7) * img.shape[0])]

    # Find the amount to add to borders
    imgL_adds = findBestAdds(img, imgL_c_x, imgL_c_y,
                             imgL_r_x, imgL_r_y, image_left=True, ds=20)
    imgL_add_x, imgL_add_y = imgL_adds[0:2], imgL_adds[2:]
    imgR_adds = findBestAdds(img, imgR_c_x, imgR_c_y,
                             imgR_r_x, imgR_r_y, image_left=False, ds=20)
    imgR_add_x, imgR_add_y = imgR_adds[0:2], imgR_adds[2:]

    # Update centers to the new rectangle
    imgL_c_x += int((imgL_add_x[1] - imgL_add_x[0]) / 2)
    imgL_c_y += int((imgL_add_y[1] - imgL_add_y[0]) / 2)
    imgR_c_x += int((imgR_add_x[1] - imgR_add_x[0]) / 2)
    imgR_c_y += int((imgR_add_y[1] - imgR_add_y[0]) / 2)

    # Update radius to the new value with add
    imgL_r_x = int(((imgL_add_x[1] + imgL_r_x[1]) +
                   (imgL_add_x[0] + imgL_r_x[0])) / 2)
    imgL_r_y = int(((imgL_add_y[1] + imgL_r_y[1]) +
                   (imgL_add_y[0] + imgL_r_y[0])) / 2)
    imgR_r_x = int(((imgR_add_x[1] + imgR_r_x[1]) +
                   (imgR_add_x[0] + imgR_r_x[0])) / 2)
    imgR_r_y = int(((imgR_add_y[1] + imgR_r_y[1]) +
                   (imgR_add_y[0] + imgR_r_y[0])) / 2)

    r_x = min(imgL_r_x, imgR_r_x)
    r_y = min(imgL_r_y, imgR_r_y)

    # Get our image through its boundaries
    imgL = img[(imgL_c_y - r_y): (imgL_c_y + r_y),
               (imgL_c_x - r_x): (imgL_c_x + r_x), :]
    imgR = img[(imgR_c_y - r_y): (imgR_c_y + r_y),
               (imgR_c_x - r_x): (imgR_c_x + r_x), :]
    imgM = img[:, (imgL_c_x + r_x): (imgR_c_x - r_x), :]

    return imgL, imgR, imgM

# Testing setup
# def main():
#     filename = sys.argv[1]
#     basepath = "imagens_stereo_IMS/"
#     outpath = "processed_data/"
#     filepath = basepath + filename + ".jpg"
#     img = cv.imread(filepath)

#     imgL, imgR, imgM = getStereoSplit(img)
#     cv.imwrite(outpath + filename + "_left.jpg", imgL)
#     cv.imwrite(outpath + filename + "_right.jpg", imgR)
#     cv.imwrite(outpath + filename + "_middle.jpg", imgM)


# if __name__ == "__main__":
#     main()
