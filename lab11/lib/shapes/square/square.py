from shapes.shape import Shape


class Square(Shape):
    def __init__(self,side):
        self.shape = "Square"
        self.side = side

    def circuit(self):
        return self.side * self.side
