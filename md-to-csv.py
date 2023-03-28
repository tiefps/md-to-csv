import argparse
import csv
import logging
import sys
from datetime import datetime
from typing import NamedTuple

import pypandoc
from bs4 import BeautifulSoup, Tag


class ParagraphRow(NamedTuple):
    h1: str
    h2: str
    h3: str
    h4: str
    h5: str
    h6: str
    p: str


parser = argparse.ArgumentParser()
parser.add_argument("input", help="markdown file to convert")
parser.add_argument("-o", "--output", help="name of output file, if unset it converts file.md to out-<ISO 8601>.csv")
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

args = parser.parse_args()

log_level = logging.DEBUG if args.verbose else logging.INFO
logging.basicConfig(stream=sys.stdout, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)
logging.debug('Running with args: %s', args)

html_doc = pypandoc.convert_file(args.input, 'html')
logging.debug('Converted to: %s', html_doc)

logging.info('Parsing HTML with BeautifulSoup')
soup = BeautifulSoup(html_doc, 'html.parser')
logging.debug('Soup: %s', soup)


def get_parent_header(t: Tag, header_name: str, previous_header_line: int, default_value='') -> (str, int):
    """Returns the header text for the tag and its line number
     or default_value and the previous header's line number
    """
    header = t.find_previous_sibling(header_name)
    if header and header.sourceline > previous_header_line:
        return header.text, header.sourceline
    else:
        return default_value, previous_header_line


def not_a_header(t: Tag) -> bool:
    return t.name not in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


logging.info('Converting soup to CSV')
rows = []
for tag in soup.find_all(not_a_header, recursive=False):
    line = 0
    h1, line = get_parent_header(tag, 'h1', line)
    h2, line = get_parent_header(tag, 'h2', line)
    h3, line = get_parent_header(tag, 'h3', line)
    h4, line = get_parent_header(tag, 'h4', line)
    h5, line = get_parent_header(tag, 'h5', line)
    h6, line = get_parent_header(tag, 'h6', line)
    row = ParagraphRow(h1, h2, h3, h4, h5, h6, tag.text)
    logging.debug('%s', row)
    rows.append(row)

csv_file_name = args.output or f'out.{datetime.now().replace(microsecond=0).isoformat()}.csv'
logging.info('Writing result to %s', csv_file_name)
with open(csv_file_name, 'w') as f:
    w = csv.writer(f)
    header_row = ParagraphRow('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p')
    w.writerow(header_row)
    w.writerows(rows)

logging.debug('Wrote %s rows', len(rows))
