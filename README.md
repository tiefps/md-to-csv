# Markdown to CSV Converter

Markdown to CSV Converter is a command-line tool that facilitates the conversion of Markdown documents into CSV files.

## Prerequisites

Ensure that you have Python 3.x installed on your system.

## Installation

### Install dependencies

Run the following command to install the required dependencies:

```shell
pip3 install -r requirements.txt
```

## Usage

Convert Markdown files to CSV with ease and customization using the following options:

```
usage: main.py [-h] [-o OUTPUT] [-p {markdown,pypandoc}] [-v] input

Convert Markdown file to CSV.

positional arguments:
  input                 Markdown file to convert

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Name of output file, if unset it converts file.md to out-<ISO 8601>.csv
  -p {markdown,pypandoc}, --parser {markdown,pypandoc}
                        Markdown parser to use
  -v, --verbose         Increase output verbosity
```

### Examples

#### Basic usage

Convert `README.md` to a CSV file using the default `pypandoc` parser:

```shell
python3 main.py README.md
```

#### Specifying the output file

Save the converted CSV file as `output.csv`:

```shell
python3 main.py input.md -o output.csv
```

#### Specifying the Markdown parser

You can choose between two parser options:

1. **Markdown parser (`markdown`)**: Utilizes the [Python markdown library](https://pypi.org/project/Markdown/). [Sample Output](README_parsed_with_markdown.csv)
2. **Pypandoc parser (`pypandoc`)**: Utilizes the [pypandoc library](https://pypi.org/project/pypandoc/), which wraps Pandoc. [Sample Output](README_parsed_with_pypandoc.csv)

The choice of parser may vary depending on the specific structure and content of the Markdown file you are converting.
We recommend trying both options and choosing the one that provides the best results for your particular document.

Example usage:

```shell
# Using the markdown parser
python3 main.py input.md --parser markdown

# Or using the pypandoc parser (default)
python3 main.py input.md --parser pypandoc
```

#### Using verbose logging

Enable verbose logging with the `-v` flag:

```shell
python3 main.py input.md -v
```

## Contributing

Found a bug or have suggestions for improvements? Feel free to [open an issue](https://github.com/tiefps/md-to-csv/issues)or [submit a pull request](https://github.com/tiefps/md-to-csv/pulls).