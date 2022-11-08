import math

from Object import *


class Camera:
    def __init__(self, position, rotation, width, height, znear, zfar, fov, forward=Matrix(4, 1, [0, 0, 1, 0])):
        self.position = Matrix(3, 1, list(position))
        self.rotation = Matrix(3, 1, list(rotation))
        self.width = width
        self.height = height
        self.znear = znear
        self.zfar = zfar
        self.fov = (math.radians(fov[0]), math.radians(fov[0]))

        rx = math.radians(self.rotation.x)
        ry = math.radians(self.rotation.y)
        rz = math.radians(self.rotation.z)
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

        self.forward = rotateTransformZ * rotateTransformY * rotateTransformX * forward

    def __str__(self):
        output = "position: " + str(self.position.x) \
                 + ", " + str(self.position.y) \
                 + ", " + str(self.position.z) + "\n"

        output += "rotation: " + str(self.rotation.x) \
                  + ", " + str(self.rotation.y) \
                  + ", " + str(self.rotation.z) + "\n"

        output += "fov: " + str(self.fov)

        return output

    def worldToCameraSpace(self, obj):
        positionTransform = Matrix(4, 4, [
            [1, 0, 0, -self.position.x],
            [0, 1, 0, -self.position.y],
            [0, 0, 1, -self.position.z],
            [0, 0, 0, 1]
        ])
        rx = math.radians(-self.rotation.x)
        ry = math.radians(-self.rotation.y)
        rz = math.radians(-self.rotation.z)
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

        return Object(obj.position.matrix, obj.rotation.matrix, obj.scale.matrix,
                      [(rotateTransformX * rotateTransformY * rotateTransformZ * positionTransform * vert).matrix
                       for vert in obj.vertices], obj.triangles,
                      [norm.matrix for norm in obj.normals])

    def cameraSpaceToOrtho(self, obj):
        transformMatrix = Matrix(4, 4, [
            [1 / self.width, 0, 0, 0],
            [0, 1 / self.height, 0, 0],
            [0, 0, -(2 / (self.zfar - self.znear)), -((self.zfar + self.znear) / (self.zfar - self.znear))],
            [0, 0, -1, 0]
        ])

        return Object(obj.position.matrix, obj.rotation.matrix, obj.scale.matrix,
                      [(transformMatrix * vert).matrix[:2] for vert in obj.vertices], obj.triangles,
                      [norm.matrix for norm in obj.normals])

    def cameraSpaceToPerspective(self, obj):
        transformMatrix = Matrix(4, 4, [
            [1 / math.tan(self.fov[0] / 2), 0, 0, 0],
            [0, 1 / math.tan(self.fov[1] / 2), 0, 0],
            [0, 0, -(self.zfar + self.znear) / (self.zfar - self.znear), 2 * self.zfar * self.znear / (self.znear - self.zfar)],
            [0, 0, -1, 0]
        ])

        for vert in obj.vertices:
            vert.z *= -1


        transformedVert = [(transformMatrix * vert) for vert in obj.vertices]
        for vert in transformedVert:
            if vert.w != 0:
                vert.x /= vert.w
                vert.y /= vert.w
                #vert.z /= vert.w
            vert.x = (vert.x + 1) / 2
            vert.y = (vert.y + 1) / 2

        #TODO: dela z clipping ali mislim ka ne onak kak bi trebalo ak kuzis kaj ocu reci
        return Object(obj.position.matrix, obj.rotation.matrix, obj.scale.matrix,
                      [vert.matrix[:2]+[1 if vert.z < 0 or vert.z > self.zfar else 0] for vert in transformedVert],
                      obj.triangles, [norm.matrix for norm in obj.normals])
