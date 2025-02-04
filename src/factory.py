import cv2


class VideoCaptureFactory:
    """
    Factory for creating video capture objects.

    This class encapsulates the creation of a cv2.VideoCapture instance,
    abstracting the details of video file handling.
    """

    @staticmethod
    def create(source: str) -> cv2.VideoCapture:
        """
        Create and return a VideoCapture object for the given video source.

        Args:
            source (str): The path to the video file.

        Returns:
            cv2.VideoCapture: The video capture object.
        """
        return cv2.VideoCapture(source)
