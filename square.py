class square:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
    def diff(self):
        print(self.num)
        print(self.x[0]-self.y[0], self.x[1]-self.y[1])