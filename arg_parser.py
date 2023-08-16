import argparse


def parse_arguments():
    """
    Parses command-line arguments for the Markdown to CSV converter script.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Convert Markdown file to CSV.')
    parser.add_argument('input', type=str, help='Markdown file to convert')
    parser.add_argument('-o', '--output', type=str, help='Name of output file, if unset it converts file.md to out-<ISO 8601>.csv')
    parser.add_argument('-p', '--parser', type=str, choices=['markdown', 'pypandoc'], default='pypandoc', help='Markdown parser to use')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
    return parser.parse_args()
