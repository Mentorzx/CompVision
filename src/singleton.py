from typing import Optional

import imageio
import numpy as np


class VideoWriterSingleton:
    """
    Singleton class for writing video frames to a file.

    This class ensures that only one video writer instance exists during the execution.
    """

    _instance: Optional["VideoWriterSingleton"] = None

    def __new__(cls, filename: str, fps: int) -> "VideoWriterSingleton":
        if cls._instance is None:
            cls._instance = super(VideoWriterSingleton, cls).__new__(cls)
            cls._instance._initialize(filename, fps)
        return cls._instance

    def _initialize(self, filename: str, fps: int) -> None:
        """
        Initialize the video writer.
        """
        self.writer = imageio.get_writer(
            filename, fps=fps, codec="libx264", format="ffmpeg"
        )

    def append_frame(self, frame: np.ndarray) -> None:
        """
        Append a frame to the video.
        """
        self.writer.append_data(frame)

    def close(self) -> None:
        """
        Finalize and close the video writer.
        """
        self.writer.close()
