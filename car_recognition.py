import cv2
from os import system


class car_recognition():
    def __init__(self, original_frame, gray_frame):
        self.car_classifier = cv2.CascadeClassifier('./Haarcascades/haarcascade_car.xml')
        self.gray_frame = gray_frame
        self._original_frame = original_frame


    def recognize(self):
        cars = self.car_classifier.detectMultiScale(self.gray_frame, 1.3, 4)
        # Extract bounding boxes for any bodies identified
        for (x, y, w, h) in cars:
            # print y
            if y < 60:
                system("say -v Alex a car is too near you")
            cv2.rectangle(self._original_frame , (x, y), (x + w, y + h), (0, 255, 255), 4)
        return self.original_frame


    @property
    def original_frame(self):
        return self._original_frame