#/bin/bash

config_file=''
input_file=''
output_file=''

EXPECTED_ARGS=3

print_usage() {
  echo "Usage: ./run.sh -c <path_to_config_file> -i <path_to_input_file> -o <path_to_output_file>"
}

while getopts 'c:i:o:' flag; do
  case "${flag}" in
    c) config_file="${OPTARG}" ;;
    i) input_file="${OPTARG}" ;;
    o) output_file="${OPTARG}" ;;
    *) printusage && exit 1 ;;
esac
done

if [ ! -f "$config_file" ]; then
  echo "Bad file: $config_file"
  exit 1
fi

if [ ! -f "$input_file" ]; then
  echo "Bad file: $config_file"
  exit 1
fi

output_file="${output_file:-output.mp4}"

if [ -f "$output_file" ]; then
  echo "$output_file already exists"
  exit 1
fi

docker build . -t bacteria-plot

docker run --rm -it \
  -v ".:/manim" \
  --mount type=bind,source="$config_file",target="/manim/config.json" \
  --mount type=bind,source="$input_file",target="/manim/data.csv" \
  bacteria-plot

mkdir -p "$(dirname $output_file)"
cp -p ./media/videos/1080p60/DataPointsScene.mp4 "$output_file"
rm -rf ./media
