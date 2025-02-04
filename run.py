import yaml

from src.mobile_robot_estimator import MobileRobotEstimatorFacade


def load_config(path: str) -> dict:
    """Load configuration from a YAML file."""
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config


if __name__ == "__main__":
    config = load_config("config/config.yml")
    estimator = MobileRobotEstimatorFacade(
        video_file=config["video_file"],
        output_video=config["output_video"],
        info_file=config["info_file"],
        fps=config["fps"],
        sample_interval=config["sample_interval"],
    )
    estimator.run()
