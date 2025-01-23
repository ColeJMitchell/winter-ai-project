import cv2
class square:
    #Initializes the coordinate bounds of the square on the chess board
    def __init__(self, x, y, num):
        self.x = list(x)
        self.y = list(y)
        self.num = num
    
    #Prints the dimensions of the square and its number
    def show_dim(self):
        xDiff = self.x[1] - self.x[0]
        yDiff = self.y[1] - self.y[0]
        print(f"Board num: {self.num}\n X dim: {xDiff}, Y dim: {yDiff}")

    #Returns the bounds of the square
    def get_bounds(self):
        return self.x[0], self.x[1], self.y[0], self.y[1]
        
    #Finds squares that have the wrong dimensions
    def find_wrong(self):
        xDiff = self.x[1] - self.x[0]
        yDiff = self.y[1] - self.y[0]
        if xDiff != 123 or yDiff != 114:
            print(f"Board num: {self.num}\n X dim: {xDiff}, Y dim: {yDiff}")
    
    #Saves the square image for training data
    def save_image(self, image, piece_color, piece_type, square):
        print(f"Y: {self.y[0]} to {self.y[1]}, X: {self.x[0]} to {self.x[1]}")
        print(f"{self.y[1] - self.y[0]} x {self.x[1] - self.x[0]}")
        save_path = f"/home/cole/github/winter-ai-project/training_data/{piece_color}_{piece_type}/{square}.jpg"
        cv2.imwrite(save_path, image[self.y[0]:self.y[1], self.x[0]:self.x[1]])
    
    #Test Code
    def save_image2(self, image, counter):
        save_path = f"/home/cole/github/winter-ai-project/boards/{counter}.jpg"
        cv2.imwrite(save_path, image[self.y[0]:self.y[1], self.x[0]:self.x[1]])

    #Normalizes the image to 123 x 123
    def normalize(self):
        self.y[0] = self.y[0] - 9
        self.y[1] = self.y[1]
        self.x[0] = self.x[0] + 9
        self.x[1] = self.x[1] + 9