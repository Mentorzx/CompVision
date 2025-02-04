from abc import ABC, abstractmethod
from typing import Any, Callable, Tuple

import matplotlib.pyplot as plt
import numpy as np


class PlotDecorator(ABC):
    """
    Abstract decorator for matplotlib Figures.

    This decorator defines a common interface to extend plot functionalities.
    """

    def __init__(self, plot_func: Callable[..., plt.Figure]) -> None:
        self._plot_func = plot_func

    @abstractmethod
    def render(self, *args: Any, **kwargs: Any) -> plt.Figure:
        """
        Extend the plotting function to add additional visual elements.

        Returns:
            plt.Figure: The enhanced matplotlib figure.
        """
        pass


class InertiaPlotDecorator(PlotDecorator):
    """
    Decorator that adds an ellipse to represent inertia on the plot.
    """

    def render(
        self,
        centroid: Tuple[float, float],
        eigenvalues: np.ndarray,
        angle: float,
        base_fig: plt.Figure,
    ) -> plt.Figure:
        """
        Render the base figure and add an inertia ellipse.

        Args:
            centroid (Tuple[float, float]): The (x, y) centroid coordinates.
            eigenvalues (np.ndarray): The eigenvalues of the inertia matrix.
            angle (float): The angle of orientation in degrees.
            base_fig (plt.Figure): The original figure.

        Returns:
            plt.Figure: The figure with the inertia ellipse added.
        """
        ax = base_fig.axes[0]
        ellipse = plt.matplotlib.patches.Ellipse(
            centroid,
            width=np.sqrt(eigenvalues[0] * 5.991),
            height=np.sqrt(eigenvalues[1] * 5.991),
            angle=angle,
            edgecolor="c",
            linewidth=2,
            fill=False,
            label="Inertia",
        )
        ax.add_patch(ellipse)
        return base_fig
