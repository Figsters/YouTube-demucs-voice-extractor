# YouTube Demucs Voice Extractor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

This project is a Python script that allows you to extract voice tracks from YouTube videos using Demucs https://github.com/facebookresearch/demucs, a state-of-the-art source separation algorithm. It provides a simple and efficient way to obtain isolated voice tracks from complex music mixes.

The script takes a YouTube video URL or a list of URLs from an Excel file as input and outputs the extracted voice tracks as separate audio files. 

## Requirements

- Python 3.x
- Demucs package (`pip install demucs`)
- FFMPEG (`sudo apt-get install ffmpeg` on Linux or download from [ffmpeg.org](https://ffmpeg.org/download.html) on other platforms)

## Usage

1. Install the required packages as mentioned in the Requirements section.
2. Clone this repository or download the `demucs_voice_extractor.py` file.
3. Open your terminal or command prompt and navigate to the directory containing the `demucs_voice_extractor.py` file.
4. Run the script using the following command: `python script.py file_path`.
    - The `file_path` argument can be a single YouTube video URL or an Excel file containing a list of URLs.
5. Wait for the script to finish processing. The extracted voice tracks will be saved in the specified output folder.
    - The output files will be saved in the output directory named as same as excel file or requested as Artist Name, which will be created in the same directory as the script.py file. The extracted audio files will be in .wav format and will be 15 seconds lenght.
## Contributing

Contributions to this project are welcome. To contribute, please fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact

If you have any questions or issues, please contact emacam01@gmail.com.