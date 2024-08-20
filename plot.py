import csv
import os
import json
from argparse import ArgumentParser
from typing import Tuple
from config import Config

from scene import DataPointsScene


def parse_arguments() -> Tuple[str]:
    parser = ArgumentParser(
        description="Create a graph animation from data points",
    )
    parser.add_argument(
        "data_file_path",
        type=str,
        help="The path to the CSV file containing the data",
    )
    parser.add_argument(
        "config_file",
        type=str,
        help="The path to the configuration file of the program"
    )

    args = parser.parse_args()
    return (args.data_file_path, args.config_file)

def read_configuration(config_file_path: str):
    with open(config_file_path, mode='r') as conf_file:
        config_json = json.loads(conf_file.read())
    return Config(**config_json)

def main():
    (data_file_path, config_file_path) = parse_arguments()

    if not os.path.isfile(data_file_path):
        print(f"{data_file_path} is not a file... :(")
        exit(1)

    if not os.path.isfile(config_file_path):
        print(f"{config_file_path} is not a file... :(")
        exit(1)

    config = read_configuration(config_file_path)

    with open(data_file_path, mode="r", newline="") as data_file:
        csv_reader = csv.DictReader(data_file, delimiter=config.data.delimiter)

        data_points = [
            {key: float(value) for key, value in row.items()} for row in csv_reader
        ]

        scene = DataPointsScene(
            data_points=data_points,
            config=config
        )
        scene.render()


if __name__ == "__main__":
    main()
