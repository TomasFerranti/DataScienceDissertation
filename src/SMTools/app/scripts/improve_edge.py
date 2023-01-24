"""
improve_edge.py is an optimized set of scripts with numba in order to find the best
pixels for an edge in order to maximize the sum of edge detection pixels across the segment
"""
import matplotlib.pyplot as plt
import cv2 as cv
import numpy as np
from scipy.ndimage import gaussian_filter
from numba import jit


def toRGB(image):
    """
    toRGB transforms a grey image with values in [0,1] to an RGB image with int values in [0,255]

    Parameters
    - image:np.array, float of shape (m,n)

    Return
    - :np.array, uint8 of shape (m,n,3)
    """
    image = np.round(255 * image)
    return np.concatenate(3 * [image.reshape((image.shape[0], image.shape[1], 1))], axis=2).astype(np.uint8)


@jit(nopython=True)
def optimizePoints(p0_list, p1_list, edges):
    """
    optimizePoints iterates over a list of points p0 and p1 to find the best pair in 
    a [0,1] matrix of edges detection

    Parameters
    - p0_list:list, list of lists of len 2 of coordinates x,y
    - p1_list:list, list of lists of len 2 of coordinates x,y
    - edges:np.array, of shape (m,n) of [0,1] values

    Return
    - best_p0:list, list of len 2 indicating x,y
    - best_p1:list, list of len 2 indicating x,y
    - best_score:float, best score found in optimization step
    """
    best_score = 0
    best_p0 = None
    best_p1 = None
    for cur_p0 in p0_list:
        for cur_p1 in p1_list:
            x0, y0, x1, y1 = cur_p0[0], cur_p0[1], cur_p1[0], cur_p1[1]

            # SOURCE BEGIN
            # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
            dx = abs(x1 - x0)
            sx = 1 if x0 < x1 else -1
            dy = -abs(y1 - y0)
            sy = 1 if y0 < y1 else -1
            error = dx + dy

            xcoordinates = []
            ycoordinates = []
            while True:
                xcoordinates.append(x0)
                ycoordinates.append(y0)
                if x0 == x1 and y0 == y1:
                    break
                e2 = 2 * error
                if e2 >= dy:
                    if x0 == x1:
                        break
                    error = error + dy
                    x0 = x0 + sx
                if e2 <= dx:
                    if y0 == y1:
                        break
                    error = error + dx
                    y0 = y0 + sy
            # SOURCE END

            score = 0
            for i in range(len(xcoordinates)):
                score += edges[ycoordinates[i], xcoordinates[i]]
            score = score / len(xcoordinates)

            if score > best_score:
                best_score = score
                best_p0 = cur_p0
                best_p1 = cur_p1
    return best_p0, best_p1, best_score


def segsPlot(p0, p1, best_p0, best_p1, edgesMatrix, image, fig_size=(20, 10)):
    """
    segsPlot creates a matplotlib image with the comparison between previous edge and its improved version

    Parameters
    - p0:list, x,y of old p0
    - p1:list, x,y of old p1
    - best_p0:list, x,y of new p0
    - best_p1:list, x,y of new p1
    - edgesMatrix:np.array, [0,1] array of shape (m,n)
    - image:np.array, array of shape (m,n,3) indicating RGB image
    - fig_size:tuple, size of figure

    Return
    - :None
    """
    fig, axs = plt.subplots(2, 1, figsize=fig_size, dpi=80)
    min_x = min(int(np.min([best_p0[0], best_p1[0]]) - 10),
                int(np.min([p0[0], p1[0]]) - 10))
    min_y = min(int(np.min([best_p0[1], best_p1[1]]) - 10),
                int(np.min([p0[1], p1[1]]) - 10))
    max_x = max(int(np.max([best_p0[0], best_p1[0]]) + 10),
                int(np.max([p0[0], p1[0]]) + 10))
    max_y = max(int(np.max([best_p0[1], best_p1[1]]) + 10),
                int(np.max([p0[1], p1[1]]) + 10))

    previous_edge = {'x': [p0[0] - min_x, p1[0] - min_x],
                     'y': [p0[1] - min_y, p1[1] - min_y]}
    improved_edge = {'x': [best_p0[0] - min_x, best_p1[0] - min_x],
                     'y': [best_p0[1] - min_y, best_p1[1] - min_y]}

    axs[0].imshow(image[min_y:max_y, min_x:max_x, :])
    axs[0].plot(previous_edge['x'], previous_edge['y'], c='r')
    axs[0].plot(improved_edge['x'], improved_edge['y'], c='y')

    axs[1].imshow(toRGB(edgesMatrix[min_y:max_y, min_x:max_x]))
    axs[1].plot(previous_edge['x'], previous_edge['y'], c='r')
    axs[1].plot(improved_edge['x'], improved_edge['y'], c='g')

    plt.subplots_adjust(left=None, bottom=None, right=None,
                        top=None, wspace=None, hspace=None)
    plt.tight_layout()
    plt.show()


def bresenham(p0, p1):
    """
    bresenham returns an array of pixels between points p0 and p1 according to bresenham algorithm

    Parameters
    - p0:list, of len 2 indicating x,y
    - p1:list, of len 2 indicating x,y

    Return
    - p_array:np.array, of shape (n,2) indicating the n pixels between p0 and p1
    """
    # SOURCE BEGIN
    # https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    x0, y0 = p0
    x1, y1 = p1

    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)

    dx = abs(x1 - x0)
    sx = 1 if x0 < x1 else -1
    dy = -abs(y1 - y0)
    sy = 1 if y0 < y1 else -1
    error = dx + dy

    xcoordinates = []
    ycoordinates = []
    while True:
        xcoordinates.append(x0)
        ycoordinates.append(y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx
        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy
    # SOURCE END
    xcoordinates = np.array(xcoordinates).reshape(-1, 1)
    ycoordinates = np.array(ycoordinates).reshape(-1, 1)
    p_array = np.concatenate([xcoordinates, ycoordinates], axis=1)
    return p_array


def createPointsOrt(p0, p1, radius):
    """
    createPointsOrt returns two sets of orthogonal points to the line segment defined by p0 and p1, using
    the parameter radius to set the distance

    Parameters
    - p0:list, of len 2 indicating x,y
    - p1:list, of len 2 indicating x,y
    - radius:float

    Return
    - p0_arr:np.array, indicates points to test in neighbourhood of p0
    - p1_arr:np.array, indicates points to test in neighbourhood of p1
    """
    sub = (p0 - p1)
    unit_vec = sub / np.linalg.norm(sub)
    unit_vec = np.array([-unit_vec[1], unit_vec[0]])

    p0_up = np.round(p0 + radius * unit_vec)
    p0_down = np.round(p0 - radius * unit_vec)
    p0_arr = bresenham(p0_up, p0_down)

    p1_up = np.round(p1 + radius * unit_vec)
    p1_down = np.round(p1 - radius * unit_vec)
    p1_arr = bresenham(p1_up, p1_down)

    return p0_arr.astype(np.int32), p1_arr.astype(np.int32)


def cannyGaussian(img):
    """
    cannyGaussian uses Canny edge detection algorithm and gaussian blur to find edges matrix of an img

    Parameters
    - img:np.array, of shape (m,n,3)

    Return
    - edgesMatrix:np.array, a numpy array indicating edges likelihood on a scale [0,1] of shape (m,n)
    """
    mid = cv.Canny(img, 30, 150)

    edgesPre = (mid / 255)
    s = 1
    w = 5
    t = (((w - 1) / 2) - 0.5) / s
    edgesMatrix = gaussian_filter(edgesPre, sigma=s, truncate=t)
    return edgesMatrix


def improveEdges(img, edges, plot=False, edgesMatrix=None):
    """
    improveEdges merges all previous functions into a pipeline to, given an image and a list of edges, optimize
    each one with edgesMatrix as edge likelihood

    Parameters
    - img:np.array, of shape (m,n,3)
    - edges:list, list of len number of edges, where each item are two points x,y on list, e.g. [[[], []], [[], []], ...]
    - plot:bool, to plot or not the result
    - edgesMatrix:np.array, of shape (m,n), has values on [0,1] for edge likelihood

    Return
    - improvedEdges:list, list of len number of edges, where each item are two points x,y on list, e.g. [[[], []], [[], []], ...]
    """
    height = img.shape[0]
    width = img.shape[1]

    if type(edgesMatrix) == type(None):
        edgesMatrix = cannyGaussian(img)

    improvedEdges = []
    for p0, p1 in edges:
        p0 = np.array(p0)
        p1 = np.array(p1)
        best_score = 0
        best_p0 = p0
        best_p1 = p1
        rOrt = np.ceil(min(width, height) / 100)
        p0_listOrt, p1_listOrt = createPointsOrt(p0, p1, rOrt)
        best_p0, best_p1, best_score = optimizePoints(
            p0_listOrt, p1_listOrt, edgesMatrix)
        improvedEdges.append([list(best_p0), list(best_p1)])

        if plot:
            print("stereo shape:", img.shape)
            print("edge map shape:", edgesMatrix.shape)
            print("rOrt:", rOrt)
            print("p0:", p0)
            print("p1:", p1)
            print("best p0:", best_p0)
            print("best p1:", best_p1)
            print("best score:", best_score)
            print("---------------------------")
            segsPlot(p0, p1, best_p0, best_p1, edgesMatrix, img, (20, 5))

    return improvedEdges
