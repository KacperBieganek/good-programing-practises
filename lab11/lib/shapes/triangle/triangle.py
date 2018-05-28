from shapes.shape import Shape


class Triangle(Shape):
    def __init__(self, side1, side2, side3):
        self.shape = "Triangle"
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def circuit(self):
        print(str(self.side1 + self.side2 + self.side3))
