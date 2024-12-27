import cv2

def main():
    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()