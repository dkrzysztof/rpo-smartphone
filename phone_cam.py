import requests
import cv2
import numpy as np

url = "http://192.168.8.104:8080/shot.jpg"

while True:
    img_resp = requests.get(url, timeout=5)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = cv2.resize(img, (1280, 720))
    cv2.imshow("Phone Cam", img)

    if cv2.waitKey(1) == 27:
        break