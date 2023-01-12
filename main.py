import time

import cv2
import time
from Camera import *
from Shading import *


def orientation(tri):
    return (tri[2][1] - tri[1][1]) * (tri[1][0] - tri[0][0]) - (tri[1][1] - tri[0][1]) * (tri[2][0] - tri[1][0])


file = open("teapot.obj.txt", "r")
verts = []
tris = []
norms = []
lines = file.read().split("\n")

for line in lines:
    if line.split()[0] == "v":
        verts.append(tuple([float(i) for i in line.split()[1:]]))
    else:

        tris.append(tuple([int(i) - 1 for i in line.split()[1:]]))
        p1 = Matrix(3, 1, list(verts[tris[-1][0]]))
        p2 = Matrix(3, 1, list(verts[tris[-1][1]]))
        p3 = Matrix(3, 1, list(verts[tris[-1][2]]))
        norms.append(tuple(Matrix.cross(p2 - p1, p3 - p1).matrix))

teapot = Object((0, 0, 0), (0, 0, 0), (1, -1, 1), verts, tris, norms)

kocka = Object((0, 0, 0), (0, 0, 0), (5, 5, 5),
               [(-0.5, -0.5, -0.5),
                (0.5, -0.5, -0.5),
                (-0.5, 0.5, -0.5),
                (0.5, 0.5, -0.5),
                (-0.5, -0.5, 0.5),
                (0.5, -0.5, 0.5),
                (-0.5, 0.5, 0.5),
                (0.5, 0.5, 0.5)],
               [(0, 1, 2), (1, 3, 2), (0, 5, 1), (1, 7, 3), (2, 3, 6), (0, 2, 4),
                (4, 7, 5), (4, 6, 7), (0, 4, 5), (2, 6, 4), (3, 7, 6), (1, 5, 7)],
               [(0, 0, -1), (0, 0, -1), (0, -1, 0), (1, 0, 0,), (0, 1, 0), (-1, 0, 0),
                (0, 0, 1),  (0, 0, 1),  (0, -1, 0), (-1, 0, 0,), (0, 1, 0), (1, 0, 0)])

cam = Camera((0, -3, -5), (-30, 0, 0), 20, 20, .1, 100, (90, 90))

#TODO: skuzi kaj je ew(center of projection in world coordinates)
shading = Shading(2, 5, Matrix(3, 1, [5, 10, -5]),
                  Matrix(3, 1, [cam.position.x, cam.position.y, (cam.position.z + cam.zfar) / 2]), 20, 3, 1, 1)

while True:
    #za micanje kamere
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == ord('w'):
        cam.position.z += 1
    elif key == ord('s'):
        cam.position.z -= 1
    elif key == ord('a'):
        cam.position.x += 1
    elif key == ord('d'):
        cam.position.x -= 1
    elif key == ord('e'):
        cam.position.y += 1
    elif key == ord('q'):
        cam.position.y -= 1
    elif key == ord('i'):
        cam.rotation.x += 3
    elif key == ord('k'):
        cam.rotation.x -= 3
    elif key == ord('j'):
        cam.rotation.y += 3
    elif key == ord('l'):
        cam.rotation.y -= 3
    elif key == ord('o'):
        cam.rotation.z += 3
    elif key == ord('u'):
        cam.rotation.z -= 3

    teapot.rotation.y += 30
    worldSpaceObj = Object.objectToWorldSpace(teapot)
    camSpaceObj = cam.worldToCameraSpace(worldSpaceObj)
    onScreen = cam.cameraSpaceToPerspective(camSpaceObj)

    img = numpy.ones((1000, 1000, 3), numpy.uint8)*255

    # redoslijed v kojemu se renderaju trianglei, sortiramo po prosjecnome .z vertecii v kamera spaceu
    seqence = [i for i in range(len(onScreen.triangles))]
    seqence = sorted(seqence, key=lambda x: camSpaceObj.vertices[onScreen.triangles[x][0]].z +
                                            camSpaceObj.vertices[onScreen.triangles[x][1]].z +
                                            camSpaceObj.vertices[onScreen.triangles[x][2]].z)
    for i in seqence:
        # .z je 1 ako je izvan clipping planei, a inace 0
        if onScreen.vertices[onScreen.triangles[i][0]].z or onScreen.vertices[onScreen.triangles[i][1]].z \
           or onScreen.vertices[onScreen.triangles[i][2]].z:
            continue

        polygon = numpy.array([
            [onScreen.vertices[onScreen.triangles[i][0]].x, onScreen.vertices[onScreen.triangles[i][0]].y],
            [onScreen.vertices[onScreen.triangles[i][1]].x, onScreen.vertices[onScreen.triangles[i][1]].y],
            [onScreen.vertices[onScreen.triangles[i][2]].x, onScreen.vertices[onScreen.triangles[i][2]].y]
        ]) * 1000  # mnozimo sa dimenzijom slike

        ori = orientation(polygon)
        # dot = -Matrix.dot(onScreen.normals[i].normalize(), Matrix(4, 1, [1, 1, 1, 0]).normalize())
        center = worldSpaceObj.vertices[onScreen.triangles[i][0]] + \
                 worldSpaceObj.vertices[onScreen.triangles[i][1]] + \
                 worldSpaceObj.vertices[onScreen.triangles[i][2]]
        center = Matrix(3, 1, [i / 3 for i in center.matrix[:3]])
        currColor = shading.calculateFaceColor(center,
                                               Matrix(3, 1, worldSpaceObj.normals[i].matrix[:3]))

        # backface culling
        if ori > 0:                                         # PAZI: BGR color
            cv2.fillPoly(img, numpy.int32([polygon]), color=(min(255, int(currColor * 156 / 255)),
                                                             min(255, int(currColor * 240 / 255)),
                                                             min(255, int(currColor * 31 / 255))))
            #cv2.polylines(img, numpy.int32([polygon]), True, color=(0, 0, 0), thickness=1)

    cv2.imshow('image', img)


cv2.destroyAllWindows()
