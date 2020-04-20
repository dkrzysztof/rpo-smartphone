import requests
import cv2
import imutils
import time
import datetime
import numpy as np
from tkinter import messagebox
from PIL import Image

class MotionDetectorContour:
    def __init__(self,dynamic=False,ceil=50):
        self.ceil = ceil
        self.dynamic = dynamic
        self.url = "http://192.168.8.107:8080/shot.jpg"

    def getFrame(self):
        img_resp = requests.get(self.url, timeout=5)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
        img = cv2.imdecode(img_arr, -1)
        return img

    def run(self):
        firstFrame = None

        while True:
            # Pobranie ramki i dostosowanie rozmiaru
            frame = self.getFrame()
            frame = imutils.resize(frame, width=500)
            text = "Brak ruchu"

            # Skala szarosci i rozmazanie
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # Przypisanie pierwszej ramki jesli jest pusta
            if firstFrame is None:
                firstFrame = gray
                continue

            # Roznica pomiedzy obecna i pierwsza ramka
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # Wyszukanie konturow poruszajacego sie obiektu
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Przejscie po wszystkich konturach
            for c in cnts:
		        # Zignoruj obiekt, jesli jest za maly
                if cv2.contourArea(c) < self.ceil:
                    continue

                # Przelicz obramowke wokol konturu
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Wykryto ruch!"

            # Tekst i data na ramce
            cv2.putText(frame, "Status: {}".format(text), (10, 20),
		    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            # Wyswietl ramki
            cv2.imshow("Security Feed", frame)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)

            # Czy wykrywanie ruchu jest dynamiczne
            if self.dynamic:
                firstFrame = gray

            # Listen for ESC or ENTER key
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break   


if __name__=="__main__":
    answer = messagebox.askyesno("Rodzaj wykrywania ruchu", "Czy wykrywanie ruchu powinno byc dynamiczne?")
    print(answer)
    t = MotionDetectorContour(answer)
    t.run()