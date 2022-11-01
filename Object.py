import math
from Matrix import *


# klasa koja predstavlja jedan objekt, npr. kocka
class Object:
    # pozicija u world space-u, rotacija(Euler angles), velicina, vrhovi, bridovi
    def __init__(self, position, rotation, scale, vertices, triangles, normals):
        self.position = Matrix(4, 1, list(position) + [1])
        self.rotation = Matrix(4, 1, list(rotation) + [1])
        self.scale = Matrix(4, 1, list(scale) + [1])

        self.vertices = []
        for vert in vertices:
            self.vertices.append(Matrix(4, 1, list(vert) + ([1] if len(list(vert)) == 3 else [])))
        self.triangles = triangles
        self.normals = []
        for norm in normals:
            self.normals.append(Matrix(4, 1, list(norm) + ([0] if len(list(norm)) == 3 else [])))
        for i in range(len(self.normals)):
            self.normals[i] = self.normals[i].normalize()

    def __str__(self):
        output = "position: " + str(self.position.x)\
                  + ", " + str(self.position.y)\
                  + ", " + str(self.position.z) + "\n"

        output += "rotation: " + str(self.rotation.x)\
                  + ", " + str(self.rotation.y)\
                  + ", " + str(self.rotation.z) + "\n"

        output += "scale: " + str(self.scale.x)\
                  + ", " + str(self.scale.y)\
                  + ", " + str(self.scale.z) + "\n"

        output += "vertices:\n"
        for vert in self.vertices:
            for coord in vert.matrix:
                output += str(round(coord, 2)) + " "
            output += "\n"
        output += "triangles:\n"
        for triangle in self.triangles:
            output += str(triangle[0]) + ", " + str(triangle[1]) + ", " + str(triangle[2]) + "\n"
        output += "normals:\n"
        for norm in self.normals:
            for axis in norm.matrix:
                output += str(round(axis, 2)) + " "
            output += "\n"

        return output

    @staticmethod
    def objectToWorldSpace(object):
        positionTransform = Matrix(4, 4, [
            [1, 0, 0, object.position.x],
            [0, 1, 0, object.position.y],
            [0, 0, 1, object.position.z],
            [0, 0, 0, 1]
        ])
        rx = math.radians(object.rotation.x)
        ry = math.radians(object.rotation.y)
        rz = math.radians(object.rotation.z)
        rotateTransformX = Matrix(4, 4, [
            [1, 0, 0, 0],
            [0, math.cos(rx), -math.sin(rx), 0],
            [0, math.sin(rx), math.cos(rx), 0],
            [0, 0, 0, 1]
        ])
        rotateTransformY = Matrix(4, 4, [
            [math.cos(ry), 0, math.sin(ry), 0],
            [0, 1, 0, 0],
            [-math.sin(ry), 0, math.cos(ry), 0],
            [0, 0, 0, 1]
        ])
        rotateTransformZ = Matrix(4, 4, [
            [math.cos(rz), -math.sin(rz), 0, 0],
            [math.sin(rz), math.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        scaleTransform = Matrix(4, 4, [
            [object.scale.x, 0, 0, 0],
            [0, object.scale.y, 0, 0],
            [0, 0, object.scale.z, 0],
            [0, 0, 0, 1]
        ])

        return Object(object.position.matrix, object.rotation.matrix, object.scale.matrix,
                      [(positionTransform * rotateTransformZ * rotateTransformY *
                       rotateTransformX * scaleTransform * vert).matrix for vert in object.vertices],
                      object.triangles, [(positionTransform * rotateTransformZ * rotateTransformY *
                       rotateTransformX * scaleTransform * norm).matrix for norm in object.normals])
