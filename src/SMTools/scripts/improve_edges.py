"""
improve_edges.py makes a routine involving the edge improvent algorithm from improve_edge.py
"""
import matplotlib.pyplot as plt
import copy

from scripts.improve_edge import improveEdges, cannyGaussian
from scripts.shared_functions import readImage, saveToFile, readJson, createImageDict


def improveEdgesDict(img_dict, img_calib):
    """
    improveEdgesDict takes parameters about an image and its calibration and optimize each calibration segment

    Parameters
    - img_dict:dict, object with data about an image and its parameters
    - img_calib:dict, object with data about an image calibration 

    Return
    - img_calib_improved:dict, object with data about an image calibration with segments improved
    """
    img_calib_improved = copy.deepcopy(img_calib)
    edgesMatrix = cannyGaussian(img_dict['img'])
    cEscala, wInicio, hInicio = img_dict['cEscala'], img_dict['wInicio'], img_dict['hInicio']

    for i in range(0, 3):
        img_calib_improved['pontosguia'][i] = [[int((1 / cEscala) * (x - wInicio)),
                                                int((1 / cEscala) * (y - hInicio))]
                                               for x, y in img_calib_improved['pontosguia'][i]]

        edges = [[img_calib_improved['pontosguia'][i][2*j],
                  img_calib_improved['pontosguia'][i][2*j + 1]]
                 for j in range(int(len(img_calib_improved['pontosguia'][i]) / 2))]

        best_edges = improveEdges(
            img_dict['img'], edges, plot=False, edgesMatrix=edgesMatrix)

        img_calib_improved['pontosguia'][i] = [
            point for edge in best_edges for point in edge]
        img_calib_improved['pontosguia'][i] = [[int(cEscala * x + wInicio), int(cEscala * y + hInicio)]
                                               for x, y in img_calib_improved['pontosguia'][i]]
    return img_calib_improved


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


def plotImprovement(img_dict, img_calib, img_calib_improved):
    """
    plotImprovement creates a plot comparing calibration segments before and after improvement

    Parameters
    - img_dict:dict, object with data about an image and its parameters
    - img_calib:dict, object with data about an image calibration 
    - img_calib_improved:dict, object with data about an image calibration with segments improved

    Return
    - :None
    """
    img = img_dict["img_canvas"].copy()
    fig, axs = plt.subplots(1, 2, figsize=(10, 20), dpi=80)
    axs[0].imshow(img)
    axs[1].imshow(img)
    for i, c in enumerate(['r', 'g', 'b']):
        edges = [[img_calib['pontosguia'][i][2*j], img_calib['pontosguia'][i][2*j + 1]]
                 for j in range(len(img_calib['pontosguia'][i]) // 2)]
        edges_improved = [[img_calib_improved['pontosguia'][i][2*j], img_calib_improved['pontosguia'][i][2*j + 1]]
                          for j in range(len(img_calib_improved['pontosguia'][i]) // 2)]
        for p0, p1 in edges:
            plotEdge(p0, p1, c, axs[0])
        for p0, p1 in edges_improved:
            plotEdge(p0, p1, c, axs[1])
    plt.show()


def improveJsonEdges(img_calib, img, plot=True):
    """
    improveJsonEdges takes a calibration and an image and improves the segments inside the img pixels

    Parameters
    - img_calib:dict, object with data about an image calibration 
    - img:np.array, 
    - plot:bool, to plot improvement

    Return
    - img_calib_improved:dict, object with data about an image calibration with segments improved
    """
    img_dict = createImageDict(img)
    img_calib_improved = improveEdgesDict(img_dict, img_calib)
    if plot:
        plotImprovement(img_dict, img_calib, img_calib_improved)

    return img_calib_improved


# Testing setup
# def main():
#     filename = sys.argv[1]
#     img_calib = readJson(filename)
#     img = readImage(img_calib, 'processed_data/')
#     img_calib = improveJsonEdges(img_calib, img)
#     filepath_save = "processed_data/" + img_calib['nomeImagem'] + ".json"
#     saveToFile(img_calib, filepath_save)


# if __name__ == "__main__":
#     main()
