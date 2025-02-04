from abc import ABC, abstractmethod

import cv2
import numpy as np


class ThresholdStrategy(ABC):
    """
    Abstract base class for thresholding strategies.

    Defines the interface for converting a frame into a binary image.
    """

    @abstractmethod
    def apply(self, frame: np.ndarray) -> np.ndarray:
        """
        Apply a thresholding algorithm to the input frame.

        Args:
            frame (np.ndarray): The input color image frame.

        Returns:
            np.ndarray: The thresholded binary image.
        """
        pass


class RedColorThresholdStrategy(ThresholdStrategy):
    """
    Concrete strategy that applies a red color-based threshold.

    This strategy computes the red chromaticity of the frame and thresholds
    based on pre-defined limits.
    """

    def apply(self, frame: np.ndarray) -> np.ndarray:
        """
        Convert the input frame to a binary image highlighting red regions.

        Args:
            frame (np.ndarray): The input color image frame.

        Returns:
            np.ndarray: The binary image after thresholding.
        """
        R = frame[:, :, 2].astype(np.float32)
        G = frame[:, :, 1].astype(np.float32)
        B = frame[:, :, 0].astype(np.float32)
        Y = R + G + B
        r = np.divide(R, Y, out=np.zeros_like(R), where=Y != 0)
        g = np.divide(G, Y, out=np.zeros_like(G), where=Y != 0)
        binary = ((r >= 0.5) & (g <= 0.2)).astype(np.uint8) * 255
        return binary
