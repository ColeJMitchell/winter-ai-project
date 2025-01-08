import cv2
class square:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
    def diff(self):
        xDiff = self.x[1] - self.x[0]
        yDiff = self.y[1] - self.y[0]
        print(f"Board num: {self.num}\n X dim: {xDiff}, Y dim: {yDiff}")
    def findWrong(self):
        xDiff = self.x[1] - self.x[0]
        yDiff = self.y[1] - self.y[0]
        if xDiff != 123 or yDiff != 114:
            print(f"Board num: {self.num}\n X dim: {xDiff}, Y dim: {yDiff}")
    def saveImage(self, image):
        cv2.imwrite(f"dataset/square_{self.num}.jpg", image)
            