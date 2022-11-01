from Object import *


class Camera:
    def __init__(self, position, rotation, width, height, znear, zfar, fov, forward=Matrix(4, 1, [0, 0, 1, 0])):
        self.position = Matrix(3, 1, list(position))
        self.rotation = Matrix(3, 1, list(rotation))
        self.width = width
        self.height = height
        self.znear = znear
        self.zfar = zfar
        self.fov = fov

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
                      [(rotateTransformZ * rotateTransformY * rotateTransformX * positionTransform * vert).matrix
                       for vert in obj.vertices], obj.triangles,
                      [(positionTransform * rotateTransformZ * rotateTransformY * rotateTransformX * norm).matrix
                       for norm in obj.normals])

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
            [math.atan(self.fov[0] / 2), 0, 0, 0],
            [0, math.atan(self.fov[1] / 2), 0, 0],
            [0, 0, -((self.zfar + self.znear) / (self.zfar - self.znear)), -((2 * self.zfar * self.znear) / (self.zfar - self.znear))],
            [0, 0, -1, 0]
        ])

        transformedVert = [(transformMatrix * vert).matrix for vert in obj.vertices]
        for vert in transformedVert:
            if vert[3] != 0:
                vert[0] /= vert[3]
                vert[1] /= vert[3]
                vert[2] /= vert[3]
            vert[0] = (vert[0] + 1) / 2
            vert[1] = (vert[1] + 1) / 2
            vert[2] = (vert[2] + 1) / 2

        return Object(obj.position.matrix, obj.rotation.matrix, obj.scale.matrix,
                      [vert[:2]+[1 if vert[2] < self.znear or vert[2] > self.zfar else 0] for vert in transformedVert],
                      obj.triangles, [norm.matrix for norm in obj.normals])
