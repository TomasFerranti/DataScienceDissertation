"""
camera_calibration.py is a collection of functions which enable the 
camera calibration through a dictionary of orthogonal line segments
for each axis X, Y, Z
"""
import sys
import numpy as np

from scripts.shared_functions import saveToFile, readJson


def getCalibType(img_calib):
    """
    getCalibType returns the information about which calibration type is going to be employed

    Parameters
    - img_calib:dict, has key 'pontosguia' which is a list of len 3 of lists of points

    Return
    - cab_type:str, type of calibration (normal or centrado)
    - missing_idx:int, if type is centrado this is the index of the missing calibration axis
    """
    cab_type = "normal"
    missing_idx = None
    for dim in range(0, 3):
        if len(img_calib['pontosguia'][(dim) % 3]) == 0 and len(img_calib['pontosguia'][(dim + 1) % 3]) > 0 and len(img_calib['pontosguia'][(dim + 2) % 3]) > 0:
            cab_type = "centrado"
            missing_idx = dim
            break
    return cab_type, missing_idx


def triangleArea(p, q, r):
    """
    triangleArea return the area of the triangle formed by p, q, r

    Parameters
    - p,q,r:list, lists of len 2 which indicates x,y of points

    Return
    - :float, value of the triangle area
    """
    return p[0]*q[1] + q[0]*r[1] + r[0]*p[1] - p[1]*q[0] - q[1]*r[0] - r[1]*p[0]


def lineIntersection(edge1, edge2):
    """
    lineIntersection finds the point on which the input edges intersect

    Parameters
    - edge1:list, list of len 2 where each element is also a list of len 2 indicating x,y
    - edge2:list, list of len 2 where each element is also a list of len 2 indicating x,y

    Return
    - intersection_point:list, list of len 2 indicating x,y of the intersection point
    """
    p, q = edge1
    r, s = edge2
    a1 = triangleArea(p, q, r)
    a2 = triangleArea(q, p, s)
    amp = a1 / (a1 + a2)
    intersection_point = np.array(r) * (1 - amp) + np.array(s) * amp
    intersection_point = intersection_point.tolist()
    return intersection_point


def getVanishingPoints(img_calib, missing_idx):
    """
    getVanishingPoints creates pontosfuga key on data, which are the vanishing points for each axis

    Parameters
    - img_calib:dict, object with data about an image calibration, mainly pontosguia key
    - missing_idx:int, index of possible missing calibration axis 

    Return
    - :None
    """
    missing_idx_cases = {None: [0, 1, 2], 0: [1, 2], 1: [0, 2], 2: [0, 1]}
    dim_cases = missing_idx_cases[missing_idx]
    vanishing_points = []
    for dim in dim_cases:
        intersection_points = []
        edges = [[img_calib['pontosguia'][dim][2*j], img_calib['pontosguia'][dim][2*j+1]]
                 for j in range(len(img_calib['pontosguia'][dim])//2)]
        for edge_index_1 in range(len(edges)):
            for edge_index_2 in range(edge_index_1 + 1, len(edges)):
                edge1 = edges[edge_index_1]
                edge2 = edges[edge_index_2]
                intersection_points.append(lineIntersection(edge1, edge2))
        intersection_points = [np.array(p).reshape(-1, 2)
                               for p in intersection_points]
        intersection_points = np.concatenate(intersection_points, axis=0)
        vanishing_point = np.mean(intersection_points, axis=0)
        vanishing_point = vanishing_point.tolist()
        vanishing_points.append(vanishing_point)
    img_calib['pontosfuga'] = vanishing_points


def proj(Va, Vb, q):
    """
    proj projects vector Va over Vb and sums it to q

    Parameters
    - Va:list, indicating a point x,y
    - Vb:list, indicating a point x,y
    - q:list, indicating a point x,y

    Return
    - :np.array, array has shape (2,)
    """
    c = Va[0]*Vb[0] + Va[1]*Vb[1]
    v = Vb[0]*Vb[0] + Vb[1]*Vb[1]
    Vb = np.array(Vb)
    q = np.array(q)
    P = Vb * c/v
    return P + q


def addHom(arr):
    """
    addHom adds a third coordinate of value 0 to a np.array

    Parameters
    - arr:np.array, of shape (2,)

    Return
    - :np.array, of shape (3,)
    """
    return np.array([arr[0], arr[1], 0])


def getOpticalCenter(img_calib, missing_idx):
    """
    getOpticalCenter adds the keys base, centrooptico and camera do the data dictionary which
    must already contain pontosfuga

    Parameters
    - img_calib:dict, object with data about an image calibration
    - missing_idx:int, missing index of the axis on calibration

    Return
    - :None
    """
    if missing_idx == None:
        Fx, Fy, Fz = img_calib['pontosfuga']
        Fx, Fy, Fz = np.array(Fx), np.array(Fy), np.array(Fz)
        hx = proj(Fx - Fy, Fz - Fy, Fy)
        hy = proj(Fy - Fz, Fx - Fz, Fz)
        CO = np.array(lineIntersection([Fx, hx], [Fy, hy]))
    else:
        Fx, Fy = img_calib['pontosfuga']
        Fx, Fy = np.array(Fx), np.array(Fy)
        CO = np.array([1200 / 2, 800 / 2])
        n = Fy - Fx
        n = np.array([-n[1], n[0]])
        t_par = (np.linalg.norm(CO))**2 + Fx.dot(Fy) - CO.dot(Fx - Fy)
        t_par = t_par / (Fx.dot(n) - CO.dot(n))
        n = n * t_par
        Fz = CO + n
        vanishing_points = [Fx, Fy, Fz]
        cases = {0: [2, 0, 1], 1: [0, 2, 1], 2: [0, 1, 2]}
        case = cases[missing_idx]
        vanishing_points = [vanishing_points[case[dim]] for dim in range(0, 3)]
        [Fx, Fy, Fz] = vanishing_points
    z2 = ((Fx[0] - Fy[0])**2 + (Fx[1] - Fy[1])**2)
    z2 -= ((Fx[0] - CO[0])**2 + (Fx[1] - CO[1])**2)
    z2 -= ((Fy[0] - CO[0])**2 + (Fy[1] - CO[1])**2)
    z2 = -1 * np.sqrt(z2/2)
    C = np.array([CO[0], CO[1], z2])
    Fx, Fy, Fz = addHom(Fx), addHom(Fy), addHom(Fz)
    X, Y, Z = Fx - C, Fy - C, Fz - C
    X, Y, Z = X / np.linalg.norm(X), Y / \
        np.linalg.norm(Y), Z / np.linalg.norm(Z)
    baseXYZ = np.concatenate(
        [X.reshape(1, -1), Y.reshape(1, -1), Z.reshape(1, -1)], axis=1).ravel()
    img_calib["base"] = baseXYZ.tolist()
    img_calib["centrooptico"] = CO.tolist()
    img_calib["camera"] = C.tolist()


def calibrateCamera(img_calib):
    """
    calibrateCamera adds to a data read from a json calibration all data necessary for 3D modelling, whered
    data must initially have the points for each orthogonal axis

    Parameters
    - img_calib:dict, object with data about an image calibration (only calibration segments)

    Return
    - img_calib:dict, object with data about an image calibration (calibration segments + camera)
    """
    cab_type, missing_idx = getCalibType(img_calib)
    getVanishingPoints(img_calib, missing_idx)
    getOpticalCenter(img_calib, missing_idx)
    return img_calib

# Testing setup
# def main():
#     filename = sys.argv[1]
#     data = readJson(filename)
#     data = calibrateCamera(data)
#     filepath_save = "processed_data/" + data['nomeImagem'] + ".json"
#     saveToFile(data, filepath_save)


# if __name__ == "__main__":
#     main()
