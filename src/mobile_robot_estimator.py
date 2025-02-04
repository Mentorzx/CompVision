import sys
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from src.command import LogCommand
from src.factory import VideoCaptureFactory
from src.frame_processor import FrameProcessorFacade
from src.observer import CentroidTracker
from src.singleton import VideoWriterSingleton
from src.strategy import RedColorThresholdStrategy


class MobileRobotEstimatorFacade:
    """
    Facade for the entire mobile robot estimation process.

    This class encapsulates video acquisition, frame processing, video writing,
    logging, and plotting of results.
    """

    def __init__(
        self,
        video_file: str,
        output_video: str,
        info_file: str,
        fps: int,
        sample_interval: int,
    ) -> None:
        self._fps: int = fps
        self._sample_interval: int = sample_interval
        self._video_capture = VideoCaptureFactory.create(video_file)
        self._video_writer = VideoWriterSingleton(output_video, fps)
        self._processor: FrameProcessorFacade = FrameProcessorFacade(
            RedColorThresholdStrategy()
        )
        self._tracker: CentroidTracker = CentroidTracker()
        self._processor.attach_observer(self._tracker)
        self._total_distance: float = 0.0
        self._frame_count: int = 0
        self._info_file: str = info_file
        self._original_stdout = sys.stdout
        self._log_command = LogCommand(self._log_parameters)

    def _redirect_stdout(self) -> None:
        """
        Redirect the standard output to the info file.
        """
        sys.stdout = open(self._info_file, "w")

    def _restore_stdout(self) -> None:
        """
        Restore the standard output to its original stream.
        """
        sys.stdout = self._original_stdout

    def _log_parameters(self) -> None:
        """
        Log the robot parameters such as FPS, sampling interval, average speed,
        total distance, and total time to the info file.
        """
        total_time: float = self._frame_count / self._fps
        average_speed: float = (
            self._total_distance / total_time if total_time > 0 else 0
        )
        print("\n-------------------- Robot Parameters -----------------------")
        print(f"Video FPS: {self._fps} frames per second")
        print(f"Sampling Interval: every {self._sample_interval} frames")
        print(f"Average Speed: {average_speed:.2f} pixels per second")
        print(f"Total Distance: {self._total_distance:.2f} pixels")
        print(f"Total Time: {total_time:.2f} seconds")
        print("--------------------------------------------------------------")

    def _plot_trajectory(self) -> None:
        """
        Plot and save the complete trajectory of the robot.
        """
        fig, ax = plt.subplots()
        history: np.ndarray = np.array(self._tracker.get_history())
        ax.set_xlim(0, 900)
        ax.set_ylim(0, 550)
        ax.invert_yaxis()
        ax.plot(history[:, 0], history[:, 1], "ro-", label="Complete Trajectory")
        ax.scatter(
            history[:, 0],
            history[:, 1],
            facecolors="none",
            edgecolors="b",
            marker="o",
            label="Trajectory Points",
        )
        ax.set_xlabel("Horizontal Position")
        ax.set_ylabel("Vertical Position")
        ax.legend()
        plt.title("Complete Trajectory")
        plt.savefig("outputs/Robot_trajectory.png")
        plt.show()
        plt.close(fig)

    def _plot_angles(self) -> None:
        """
        Plot and save the robot orientation angle across frames.
        """
        fig, ax = plt.subplots()
        ax.plot(
            range(len(self._processor.angles)), self._processor.angles, label="Angle"
        )
        ax.set_xlabel("Frame Number")
        ax.set_ylabel("Angle (degrees)")
        ax.legend()
        plt.title("Angle in Each Frame")
        plt.savefig("outputs/Robot_angles.png")
        plt.show()
        plt.close(fig)

    def run(self) -> None:
        """
        Execute the full estimation process over the video.

        This method processes the video frames, writes the annotated frames
        to an output video, logs parameters, and generates plots.
        """
        self._redirect_stdout()
        instantaneous_speed: Optional[float] = None
        while True:
            ret, frame = self._video_capture.read()
            if not ret:
                self._video_capture.release()
                break
            if self._frame_count % self._sample_interval == 0:
                fig, speed = self._processor.process(frame)
                if speed is not None:
                    history: List[Tuple[float, float]] = self._tracker.get_history()
                    if len(history) > 1:
                        dx: float = history[-1][0] - history[-2][0]
                        dy: float = history[-1][1] - history[-2][1]
                        self._total_distance += (dx**2 + dy**2) ** 0.5
                canvas: FigureCanvas = FigureCanvas(fig)
                canvas.draw()
                image = np.array(canvas.renderer.buffer_rgba())
                self._video_writer.append_frame(image)
            self._frame_count += 1
        self._log_command.execute()
        self._video_writer.close()
        self._restore_stdout()
        self._plot_trajectory()
        self._plot_angles()
