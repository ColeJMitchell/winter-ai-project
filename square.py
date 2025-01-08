import cv2
class square:
    #Initializes the coordinate bounds of the square on the chess board
    def __init__(self, x, y, num):
        self.x = list(x)
        self.y = list(y)
        self.num = num
    
    #Prints the dimensions of the square and its number
    def showDim(self):
        xDiff = self.x[1] - self.x[0]
        yDiff = self.y[1] - self.y[0]
        print(f"Board num: {self.num}\n X dim: {xDiff}, Y dim: {yDiff}")
        
    #Finds squares that have the wrong dimensions
    def findWrong(self):
        xDiff = self.x[1] - self.x[0]
        yDiff = self.y[1] - self.y[0]
        if xDiff != 123 or yDiff != 114:
            print(f"Board num: {self.num}\n X dim: {xDiff}, Y dim: {yDiff}")
    
    #Saves the square image for training data
    def saveImage(self, image):
        cv2.imwrite(f"dataset/square_{self.num}.jpg", image[self.y[0]:self.y[1], self.x[0]:self.x[1]])
    
    #Normalizes the image to 123 x 123
    def normalize(self):
        self.y[0] = self.y[0] - 5
        self.y[1] = self.y[1] + 4