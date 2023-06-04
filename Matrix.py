import math
import numpy


# klasa matrica
class Matrix:
    def __init__(self, rows, columns, matrix):
        self.rows = rows
        self.columns = columns
        self.matrix = matrix

    def __str__(self):
        output = "(" + str(self.rows) + ", " + str(self.columns) + ")\n"
        for i in range(self.rows):
            for j in range(self.columns):
                output += str(self.matrix[i][j]) + " "
            output += "\n"

        return output

    # zbrajanje matrica
    def __add__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Trying to add matrices of different sizes")

        output = []
        # ako je vektor
        if self.columns == 1:
            for i in range(self.rows):
                output.append(self.matrix[i] + other.matrix[i])
            return Matrix(self.rows, self.columns, output)

        for i in range(self.rows):
            output.append([])
            for j in range(self.columns):
                output[i].append(self.matrix[i][j] + other.matrix[i][j])
        return Matrix(self.rows, self.columns, output)

    # oduzimanje matrica
    def __sub__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Trying to subtracrt matrices of different sizes")

        output = []
        # ako je vektor
        if self.columns == 1:
            for i in range(self.rows):
                output.append(self.matrix[i] - other.matrix[i])
            return Matrix(self.rows, self.columns, output)

        for i in range(self.rows):
            output.append([])
            if self.columns == 1: # ako je vektor
                output[i] = self.matrix[i] - other.matrix[i]
            else:
                for j in range(self.columns):
                    output[i].append(self.matrix[i][j] - other.matrix[i][j])
        return Matrix(self.rows, self.columns, output)

    # množenje matrica
    def __mul__(self, other):
        if self.columns != other.rows:
            raise Exception("Trying to multiply matrices that can't be multiplied")

        output = []
        for i in range(self.rows):
            if other.columns != 1:  # ako je matrica
                output.append([])
            for j in range(other.columns):
                element = 0
                for k in range(self.columns):
                    if other.columns != 1: #ako je matrica
                        element += self.matrix[i][k % self.columns] * other.matrix[k % other.rows][j]
                    else: #ako je vektor
                        element += self.matrix[i][k % self.columns] * other.matrix[k % other.rows]
                if other.columns != 1:  # ako je matrica
                    output[i].append(element)
                else:
                    output.append(element)
        return Matrix(self.rows, other.columns, output)

    # za lakse koristenje vektora
    @property
    def x(self):
        return self.matrix[0]
    @x.setter
    def x(self, value):
        self.matrix[0] = value

    @property
    def y(self):
        return self.matrix[1]
    @y.setter
    def y(self, value):
        self.matrix[1] = value

    @property
    def z(self):
        return self.matrix[2]
    @z.setter
    def z(self, value):
        self.matrix[2] = value

    @property
    def w(self):
        return self.matrix[3]
    @w.setter
    def w(self, value):
        self.matrix[3] = value

    @staticmethod
    def dot(vect1, vect2):
        if vect1.columns > 1 or vect2.columns > 1:
            raise Exception("Can't calculate dot product of matrices")

        return vect1.x * vect2.x + vect1.y * vect2.y + vect1.z * vect2.z

    def normalize(self):
        if self.columns > 1:
            raise Exception("Can't normalize matrices")

        length = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        if length == 0:
            return self
        self.x /= length
        self.y /= length
        self.z /= length

        return self

    @staticmethod
    def cross(a, b):
        a = Matrix.normalize(a)
        b = Matrix.normalize(b)
        return Matrix(3, 1, [(a.y * b.z) - (a.z * b.y),
                             (a.z * b.x) - (a.x * b.z),
                             (a.x * b.y) - (a.y * b.x)])
