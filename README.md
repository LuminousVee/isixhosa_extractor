# isiXhosa Content Extractor

This Python script extracts isiXhosa words, phrases, and sentences from PDF or text files. 
It's designed to help identify and collect isiXhosa content from mixed-language documents.

## Features

- Extracts isiXhosa words, phrases, and sentences
- Supports both PDF and text file inputs
- Provides page numbers for each extracted item
- Outputs results in a formatted text file

## Requirements

- Python 3.6+
- PyPDF2

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/LuminousVee/isixhosa-content-extractor.git
   cd isixhosa-content-extractor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script from the command line:

```
python isixhosa_extractor.py input_file output_file
```

- `input_file`: Path to the input PDF or text file
- `output_file`: Path where the output will be saved

Example:
```
python isixhosa_extractor.py document.pdf extracted_content.txt
```

## Output

The script generates a text file containing:

1. Extracted isiXhosa words
2. Extracted isiXhosa phrases (2-5 words)
3. Extracted isiXhosa sentences

Each item is listed with the page number(s) where it appears in the original document.

## Limitations

- The script uses a simple heuristic to identify isiXhosa content, which may not be 100% accurate.
- PDF extraction quality depends on the PDF's structure and content.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.