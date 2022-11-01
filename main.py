import cv2
import numpy
import time
from Camera import *


def orientation(tri):
    return (tri[2][1] - tri[1][1]) * (tri[1][0] - tri[0][0]) - (tri[1][1] - tri[0][1]) * (tri[2][0] - tri[1][0])


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

cam = Camera((-10, 0, 0), (0, 0, 0), 20, 20, 1, 100, (5, 5))
while True:
    #kocka.rotation.x += .4
    #kocka.rotation.y += .4
    cam.rotation.y += .4
    onScreen = cam.cameraSpaceToPerspective(cam.worldToCameraSpace(Object.objectToWorldSpace(kocka)))

    img = numpy.ones((1000, 1000, 3), numpy.uint8)*255
    for i in range(len(onScreen.triangles)):
        #.z je 1 ako je izvan clipping planei, a inace 0
        if onScreen.vertices[onScreen.triangles[i][0]].z and onScreen.vertices[onScreen.triangles[i][1]].z \
                and onScreen.vertices[onScreen.triangles[i][2]].z:
            continue
        polygon = numpy.array([
            [onScreen.vertices[onScreen.triangles[i][0]].x, onScreen.vertices[onScreen.triangles[i][0]].y],
            [onScreen.vertices[onScreen.triangles[i][1]].x, onScreen.vertices[onScreen.triangles[i][1]].y],
            [onScreen.vertices[onScreen.triangles[i][2]].x, onScreen.vertices[onScreen.triangles[i][2]].y]
        ]) * 1000

        ori = orientation(polygon)
        dot = -Matrix.dot(onScreen.normals[i].normalize(), Matrix(4, 1, [1, -1, 1, 0]).normalize())

        if ori > 0:                                         #PAZI: BGR color
            cv2.fillPoly(img, numpy.int32([polygon]), color=(int(max(dot, .15) * 103), int(max(dot, .25) * 41), int(max(dot, .15) * 255)))
            #cv2.polylines(img, numpy.int32([polygon]), True, color=(0, 0, 0), thickness=1)

    cv2.imshow('image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
