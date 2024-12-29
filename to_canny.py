import cv2
import os

def main():
    image = cv2.imread("frames/frame_11.jpg", cv2.IMREAD_GRAYSCALE)
    edges = cv2.Canny(image, 50, 150)
    while True:
        cv2.imshow("Canny Edge Detection", edges)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows


if __name__ == "__main__":
    main()