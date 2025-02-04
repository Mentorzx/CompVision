# Mobile Robot Estimation Project

This project implements a mobile robot estimation system using computer vision techniques. It processes a video of a moving robot, extracts the robot's centroid, computes motion parameters (such as trajectory, orientation, and instantaneous speed), and generates output files including a processed video, several plots, and a log file.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Overview

The project leverages multiple computer vision techniques including thresholding, morphological operations, and moment analysis to extract motion parameters from video frames. In addition, it demonstrates the use of several design patterns (Factory, Singleton, Strategy, Observer, Decorator, Command, and Facade) to build a modular, maintainable, and scalable system.

## Features

- **Video Processing Pipeline:** Captures, processes, and analyzes video frames to estimate robot motion.
- **Design Patterns:** Incorporates multiple design patterns to enforce good software engineering practices.
- **Output Generation:**  
  - Processed video with overlays (centroid, trajectory, and inertia ellipse).  
  - Plot of the complete robot trajectory.  
  - Plot of robot orientation angles per frame.  
  - Plot of X and Y positions over frames.  
  - Log file with detailed processing parameters.
- **Modular Architecture:** Code is organized into modules for easy maintenance and extensibility.
- **Configuration File:** Uses a configuration file (e.g., YAML) to control output directories and other parameters.

## Project Structure

```plaintext
project/
├── config/
│   └── config.yml         # Configuration file for output directories, video parameters, etc.
├── data/                  # Necessary data like images or videos to run the code
├── logs/                  # Logs directory
├── outputs/               # Directory where output files (video, plots, logs) are saved
├── src/
│   ├── __init__.py        # Package initializer
│   ├── factory.py         # Contains VideoCaptureFactory (Factory Pattern)
│   ├── singleton.py       # Contains VideoWriterSingleton (Singleton Pattern)
│   ├── strategy.py        # Contains ThresholdStrategy and RedColorThresholdStrategy (Strategy Pattern)
│   ├── observer.py        # Contains CentroidObserver and CentroidTracker (Observer Pattern)
│   ├── decorator.py       # Contains PlotDecorator and InertiaPlotDecorator (Decorator Pattern)
│   ├── command.py         # Contains Command and LogCommand (Command Pattern)
│   ├── frame_processor.py # Contains FrameProcessorFacade for processing video frames
│   └── mobile_robot_estimator.py  # Contains MobileRobotEstimatorFacade (Facade Pattern)
├── run.py                 # Main entry point for the project
├── requirements.txt       # Contains requirements for the project
└── README.md              # This file
```

## Requirements

The project has been tested with the following package versions:
```plaintext
contourpy==1.3.1
cycler==0.12.1
fonttools==4.55.8
imageio==2.37.0
imageio-ffmpeg==0.6.0
kiwisolver==1.4.8
matplotlib==3.10.0
numpy==2.2.2
opencv-python==4.11.0.86
packaging==24.2
pillow==11.1.0
psutil==6.1.1
pyparsing==3.2.1
python-dateutil==2.9.0.post0
PyYAML==6.0.2
six==1.17.0
```

## Instalation

1. Clone the repository
    - git clone https://github.com/yourusername/CompVision.git
    - cd CompVision.git
2. Create and activate a virtual environment (optional but recommended):
    - python -m venv venv
    - source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install the required packages:
    - pip install -r requirements.txt

## Configuration

The project uses a configuration file (for example, config/config.yml) to define parameters such as input video file, output directories, frames per second (FPS), and sample interval. An example configuration file is shown below:

```plaintext
video_file: "video1_husky.mp4"
output_video: "outputs/husky_output.mp4"
info_file: "outputs/husky_information.txt"
fps: 20
sample_interval: 50
```

## Usage

    - python run.py

This script will:
    - Capture and process the video frames.
    - Generate a processed video with overlays.
    - Create plots for the robot trajectory, orientation angles, and X-Y positions.
    - Log processing parameters to a log file.