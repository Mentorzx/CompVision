from typing import Any, List, Optional, Tuple

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from src.decorator import InertiaPlotDecorator
from src.observer import CentroidObserver, CentroidTracker
from src.strategy import ThresholdStrategy


class FrameProcessorFacade:
    """
    Facade for processing video frames and extracting robot motion parameters.

    This class integrates thresholding, morphological operations, centroid extraction,
    inertia computation, and notification to observers.
    """

    def __init__(self, threshold_strategy: ThresholdStrategy) -> None:
        self._strategy: ThresholdStrategy = threshold_strategy
        self._kernel: np.ndarray = np.ones((3, 3), dtype=np.uint8)
        self._observers: List[CentroidObserver] = []
        self.velocities: List[float] = []
        self.angles: List[float] = []

    def attach_observer(self, observer: CentroidObserver) -> None:
        """
        Attach an observer to receive centroid updates.

        Args:
            observer (CentroidObserver): The observer instance.
        """
        self._observers.append(observer)

    def _notify(self, centroid: Tuple[float, float]) -> None:
        """
        Notify all attached observers with the new centroid.

        Args:
            centroid (Tuple[float, float]): The (x, y) centroid coordinates.
        """
        for observer in self._observers:
            observer.update(centroid)

    def process(self, frame: np.ndarray) -> Tuple[plt.Figure, Optional[float]]:
        """
        Process the frame to extract motion parameters and generate a plot.

        Args:
            frame (np.ndarray): The input video frame.

        Returns:
            Tuple[plt.Figure, Optional[float]]: A tuple containing the matplotlib figure
            with the processed frame and the instantaneous speed if available.
        """
        fig, ax = plt.subplots()
        ax.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        thresholded: np.ndarray = self._strategy.apply(frame)
        morphed: np.ndarray = cv2.erode(
            cv2.dilate(thresholded, self._kernel), self._kernel
        )
        _, labels = cv2.connectedComponents(morphed)
        blobs: np.ndarray = labels > 0
        m00: float = np.sum(blobs)
        rows, cols = blobs.shape
        X, Y = np.meshgrid(np.arange(cols), np.arange(rows))
        uc: float = np.sum(X * blobs) / m00
        vc: float = np.sum(Y * blobs) / m00
        self._notify((uc, vc))
        ax.scatter(
            uc, vc, facecolors="none", edgecolors="b", marker="o", label="Centroid"
        )

        u20: float = np.sum(((X - uc) ** 2) * blobs) / m00
        u02: float = np.sum(((Y - vc) ** 2) * blobs) / m00
        u11: float = np.sum((X - uc) * (Y - vc) * blobs) / m00
        inertia_matrix: np.ndarray = np.array([[u20, u11], [u11, u02]])
        eigenvalues, eigenvectors = np.linalg.eig(inertia_matrix)
        idx_max: int = np.argmax(eigenvalues)
        angle_rad: float = np.arctan2(
            eigenvectors[1, idx_max], eigenvectors[0, idx_max]
        )
        angle_deg: float = np.rad2deg(angle_rad)
        self.angles.append(angle_deg)

        threshold = 120
        if len(self.angles) > 1:
            if abs(self.angles[-1] - self.angles[-2]) > threshold:
                self.angles[-1] = (
                    self.angles[-2]
                    + (self.angles[-3] if len(self.angles) > 2 else self.angles[-2])
                ) / 2

        decorator = InertiaPlotDecorator(lambda *args, **kwargs: fig)
        fig = decorator.render((uc, vc), eigenvalues, angle_deg, fig)

        instantaneous_speed: Optional[float] = None
        if self._observers and isinstance(self._observers[0], CentroidTracker):
            history: List[Tuple[float, float]] = self._observers[0].get_history()
            if len(history) > 1:
                history_np = np.array(history)
                ax.plot(history_np[:, 0], history_np[:, 1], "ro-", label="Trajectory")
                dx: float = history_np[-1, 0] - history_np[-2, 0]
                dy: float = history_np[-1, 1] - history_np[-2, 1]
                arrow_scale: float = 25
                ax.arrow(
                    history_np[-1, 0],
                    history_np[-1, 1],
                    dx,
                    dy,
                    head_width=arrow_scale,
                    head_length=arrow_scale * 1.5,
                    fc="g",
                    ec="g",
                )
                instantaneous_speed = np.sqrt(dx**2 + dy**2)
                self.velocities.append(instantaneous_speed)
                ax.text(
                    history_np[-1, 0] + 10,
                    history_np[-1, 1] + 10,
                    f"{instantaneous_speed:.2f} px/frame",
                    color="g",
                )
        ax.legend()
        plt.close(fig)
        return fig, instantaneous_speed
