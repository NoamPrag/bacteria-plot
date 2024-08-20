# Bacteria-Plot

## Description
A program that plots the growth of bacteria, for presentation purposes.


## Usage
```bash
git clone https://github.com/NoamPrag/bacteria-plot.git && cd bacteria-plot
chmod +x ./run.sh
./run.sh -i <data_input_file> -c <config_file> -o <output_file>
```

- Input data file is in CSV (comma-separated-values) format
    * Delimiter may be configured in configuration file
- Config file is of a JSON format, like the example in the repo (`config.json`)
- Output file is where to save the exported mp4 video

## Requirements
- [Docker](https://docs.docker.com/get-started/get-docker/)
