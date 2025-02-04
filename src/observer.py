from abc import ABC, abstractmethod
from typing import List, Tuple


class CentroidObserver(ABC):
    """
    Abstract observer interface for receiving centroid updates.
    """

    @abstractmethod
    def update(self, centroid: Tuple[float, float]) -> None:
        """
        Receive an update of the centroid coordinates.

        Args:
            centroid (Tuple[float, float]): The (x, y) coordinates of the centroid.
        """
        pass


class CentroidTracker(CentroidObserver):
    """
    Observer that tracks and records centroid positions.

    This observer maintains a history of all centroids detected across frames.
    """

    def __init__(self) -> None:
        self._history: List[Tuple[float, float]] = []

    def update(self, centroid: Tuple[float, float]) -> None:
        """
        Append the new centroid to the tracking history.

        Args:
            centroid (Tuple[float, float]): The (x, y) centroid coordinates.
        """
        self._history.append(centroid)

    def get_history(self) -> List[Tuple[float, float]]:
        """
        Get the list of tracked centroids.

        Returns:
            List[Tuple[float, float]]: The history of centroid coordinates.
        """
        return self._history
