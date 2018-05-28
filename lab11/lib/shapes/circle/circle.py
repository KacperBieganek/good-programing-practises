from shapes import Shape


class Circle(Shape):
    pi = 3.14

    def __init__(self, radius):
        self.shape = "Circle"
        self.radius = radius

    def circuit(self):
        print(str(self.radius * 2 * self.pi))
