import cv2
import numpy as np

def main():
    image = cv2.imread("frames/frame_11.jpg", cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 50, 150)
    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB) 

    while True:
        cv2.imshow("Canny Edge Detection", edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=7)
        if lines is not None: 
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(color_image, (x1, y1), (x2, y2), (0, 255, 0), 2)  

        cv2.imshow("Hough Lines", color_image) 

    cv2.destroyAllWindows()  

if __name__ == "__main__":
    main()
