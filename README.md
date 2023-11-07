# TextAlign

Crop and straighten images containing text to prepare for Optical Character Recognition

![textalign logo](/assets/textalign_logo.png)

**TextAlign** is a Python script designed to process images and extract text bounding boxes. It is useful for various applications, such as OCR preprocessing, where text alignment and cleaning are required. The script supports various image formats, including JPEG, JPG, PNG, BMP, TIFF, and TIF.

## Features

- Supports multiple image formats, including JPEG, JPG, PNG, BMP, TIFF, and TIF.
- Detects and extracts text bounding boxes.
- Provides a clean and aligned output image.
- Logs processing information for easy debugging and tracking.
- Supports batch processing of images in a specified directory.

## Prerequisites

Before using TextAlign, ensure you have the following dependencies installed:

- Python 3.x
- OpenCV (cv2) library
- NumPy library
- argparse library
- logging library
- imghdr library

You can install these libraries using pip:

```bash
pip install opencv-python-headless numpy argparse
```

## Usage

1. Clone the repository or download the script.
2. Run the script with the following command:

```bash
python textalign.py input_directory output_directory
```

Replace `input_directory` with the path to the directory containing input images and `output_directory` with the path where you want to save the processed results.

## Processing Steps

The script performs the following steps for each image:

1. Loads the image from the input directory.
2. Applies edge detection using the Canny algorithm.
3. Finds text contours in the edge image.
4. Filters out small regions to clean the image.
5. Creates a mask to isolate the text.
6. Blackens the text region while preserving the background.
7. Rotates the image to align the text horizontally.
8. Saves the processed image to the output directory.
9. Logs the processing information.

## Intermediate Files

The script generates intermediate files during processing to help you understand each step. These files have names based on the original input filename and the processing step. Intermediate files are automatically cleaned up after processing.

- `input_filename_unrotated.ext`: The unrotated version of the image.

## Logging

The script logs processing information, including errors and warnings, to a `processing.log` file. You can monitor the progress and troubleshoot any issues by checking this log file.

## Support

If you encounter any issues or have questions, please feel free to [open an issue](https://github.com/your-repo/issues).

## License

This script is provided under the MIT License. You can find the full license in the `LICENSE` file.

---

This README provides an overview of the **TextAlign** script, its features, usage, and additional information. You can use this script to process images and extract text bounding boxes with ease.
