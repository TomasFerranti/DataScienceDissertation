"""
shared_functions.py offers some utility functions such as file manipulation for all scripts
"""
import json
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def saveToFile(data, filepath):
    """
    saveToFile dumps an object data inside a given filepath

    Parameters
    - data:any dumpable object, object with data to be saved
    - filepath:str, text with the path to save the data 

    Return
    - :None
    """
    with open(filepath, 'w') as file:
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()


def readJson(filepath):
    """
    readJson returns an object data inside a given filepath of extension .json

    Parameters
    - filepath:str, text with the path to load the data 

    Return
    - data:dict, object with json data to be loaded
    """
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data


def readImage(img_calib, filepath):
    """
    readImage returns an object data inside a given filepath of extension type readable by opencv

    Parameters
    - img_calib:dict, object with data about an image calibration 
    - filepath:str, text with the path to load the data 

    Return
    - img:np.array, float of shape (m,n,3)
    """
    img_path = filepath + img_calib['nomeImagem'] + "." + img_calib['extensao']
    img = cv.imread(img_path)
    return img


def createImageDict(img):
    """
    createImageDict returns a dictionary with the original image and all needed attributes and properties as keys

    Parameters
    - img:np.array, float of shape (m,n,3)

    Return
    - img_dict:dict, object with data about an image and its parameters
    """
    iWidth, iHeight = img.shape[1], img.shape[0]
    cWidth, cHeight = 1200, 800
    wInicio = 0
    hInicio = 0
    cEscala = 0
    aspectCanvas = cWidth/cHeight
    aspectImg = iWidth/iHeight

    if (aspectCanvas > aspectImg):
        cEscala = cHeight/iHeight
        wInicio = int(np.trunc((cWidth - cEscala*iWidth)/2))
    else:
        cEscala = cWidth/iWidth
        hInicio = int(np.trunc((cHeight - cEscala*iHeight)/2))
    img_canvas = cv.resize(img, (int(cEscala*iWidth), int(cEscala*iHeight)))

    if wInicio == 0:
        white_rect = 255 * \
            np.ones(shape=(hInicio, img_canvas.shape[1], img_canvas.shape[2])).astype(
                np.uint8)
        img_canvas = np.concatenate([white_rect, img_canvas], axis=0)
    else:
        white_rect = 255 * \
            np.ones(shape=(img_canvas.shape[0], wInicio, img_canvas.shape[2])).astype(
                np.uint8)
        img_canvas = np.concatenate([white_rect, img_canvas], axis=1)

    img_dict = {}
    img_dict['img'] = img
    img_dict['img_canvas'] = img_canvas
    img_dict['cEscala'] = cEscala
    img_dict['wInicio'] = wInicio
    img_dict['hInicio'] = hInicio
    return img_dict


def plotEdge(p0, p1, color, ax):
    """
    plotEdge creates segment between points p0 and p1 of a given color on a plot ax

    Parameters
    - p0:list, of len 2
    - p1:list, of len 2
    - color:str, must be available to matplotlib
    - ax:matplotlib_class, object which indicates a plot area

    Return
    - :None
    """
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], c=color)


def plotCalibSegs(img_dict_list, img_calib_list):
    """
    plotCalibSegs creates a matplotlib plot with the calibration segments of multiple images, each on a different plot

    Parameters
    - img_dict_list:list, list of objects with data about an image and its parameters
    - img_calib_list:list, list of objects with data about an image calibration 

    Return
    - :None
    """
    fig, axs = plt.subplots(1, len(img_dict_list), figsize=(10, 20), dpi=80)
    for idx, ax in enumerate(axs):
        ax.imshow(img_dict_list[idx]["img_canvas"])
        for i, c in enumerate(['r', 'g', 'b']):
            edges = [[img_calib_list[idx]['pontosguia'][i][2*j], img_calib_list[idx]['pontosguia'][i][2*j + 1]]
                     for j in range(len(img_calib_list[idx]['pontosguia'][i]) // 2)]
            for p0, p1 in edges:
                plotEdge(p0, p1, c, ax)
    plt.show()


def getStereoFilename(filename):
    """
    getStereoFilename returns the corresponding filename of the other half of stereo images

    Parameters
    - filename:str

    Return
    - stereo_filename:str
    """
    filename_split = filename.split(sep='_')

    swap = {'left': 'right', 'right': 'left'}
    filename_split[-1] = swap[filename_split[-1]]

    stereo_filename = '_'.join(filename_split)
    return stereo_filename
