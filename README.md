# EPS to JPG Converter

A modern web application built with Streamlit that converts EPS (Encapsulated PostScript) files to JPG format.

## Features

- Simple and intuitive user interface
- Drag-and-drop file upload
- High-quality conversion
- Preview of converted images
- Direct download of converted files
- Support for various EPS file formats

## Prerequisites

- Python 3.7 or higher
- Ghostscript installed on your system

### Installing Ghostscript

#### Windows
1. Download Ghostscript from [here](https://www.ghostscript.com/releases/gsdnld.html)
2. Install it and add it to your system PATH

#### Linux
```bash
sudo apt-get install ghostscript
```

#### macOS
```bash
brew install ghostscript
```

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

3. Upload your EPS file using the file uploader

4. Click the "Convert to JPG" button

5. Preview the converted image and download it using the download button

## License

This project is licensed under the MIT License - see the LICENSE file for details. 