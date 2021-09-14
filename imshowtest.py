import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):
    # 获得图片
    ret, frame = cap.read()
    # 展示图片
    cv2.imshow("capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # 存储图片
        cv2.imwrite("camera.jpg", frame)
        break

cap.release()
cv2.destroyAllWindows()


