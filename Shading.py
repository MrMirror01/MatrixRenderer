from Matrix import Matrix


class Shading:
    def __init__(self, ambientIntensity, directionalIntensity, lightLocation, cameraPosition,
                 ambientCoeficient, diffuseCoefficient, specularCoefficient, widthOfHighlights):
        self.ambIntensity = ambientIntensity
        self.dirIntensity = directionalIntensity
        self.lightLocation = lightLocation
        self.camPosition = cameraPosition
        self.ambCoefficient = ambientCoeficient
        self.diffCoefficient = diffuseCoefficient
        self.specCoefficient = specularCoefficient
        self.widthOfHighlights = widthOfHighlights

    def calculateFaceColor(self, center, normal):
        direction = Matrix.normalize(self.lightLocation - center)
        # spremamo v varijablu zbog optimizacije
        temp = 2 * Matrix.dot(direction, normal)
        # r i c au za racunanje specular highlighti
        r = Matrix(3, 1, [-i for i in direction.matrix]) + Matrix(3, 1, [temp * i for i in normal.matrix])
        c = self.camPosition - center

        amb = self.ambIntensity * self.ambCoefficient
        diff = self.diffCoefficient * self.dirIntensity * max(0, Matrix.dot(normal, direction))
        spec = self.specCoefficient * self.dirIntensity * pow(max(0, Matrix.dot(r, c)), self.widthOfHighlights)

        return amb + diff + spec


