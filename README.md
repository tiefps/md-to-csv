# Markdown to CSV

Converts a basic Markdown file into its CSV representation

## Set up

### Install dependencies:

```shell
pip3 install -r requirements.txt
```

## Usage

```
usage: md-to-csv.py [-h] [-o OUTPUT] [-v] input

positional arguments:
  input                 markdown file to convert

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        name of output file, if unset it converts file.md to out-<ISO 8601>.csv
  -v, --verbose         increase output verbosity
```

### Minimal example

Convert a Markdown file to a CSV file named `out.YYYY-MM-DDTHH:MM:SS.csv`:

```shell
python3 md-to-csv.py README.md
```

### Full example

Convert a Markdown file to a named CSV with verbose logging enabled:

```shell
python3 md-to-csv.py README.md -o README.csv -v
```

# Want to contribute?

Submit a [PR](https://github.com/tiefps/md-to-csv) :)