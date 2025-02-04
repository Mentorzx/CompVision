import cv2


class VideoCaptureFactory:
    @staticmethod
    def create(source: str) -> cv2.VideoCapture:
        return cv2.VideoCapture(source)
