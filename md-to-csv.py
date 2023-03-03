import argparse
import csv
import logging
import sys
from datetime import datetime
from typing import NamedTuple

import markdown
from bs4 import BeautifulSoup, PageElement


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

logging.info('Reading input file: %s', args.input)
with open(args.input, 'r', encoding='utf-8') as f:
    text = f.read()
    logging.debug('File contents: %s', text)

logging.info('Converting Markdown text to HTML')
html_doc = markdown.markdown(text)
logging.debug('Converted to: %s', html_doc)

logging.info('Parsing HTML with BeautifulSoup')
soup = BeautifulSoup(html_doc, 'html.parser')
logging.debug('Soup: %s', soup)


def get_header_for_element(element: PageElement, header_name: str, default_value=''):
    """Returns the header text for the element or default_value if not found
    """
    header = element.find_previous_sibling(header_name)
    header_text = header.text if header else default_value
    return header_text


logging.info('Converting soup to CSV')
rows = []
for p in soup.find_all('p'):
    row = ParagraphRow(
        get_header_for_element(p, 'h1'),
        get_header_for_element(p, 'h2'),
        get_header_for_element(p, 'h3'),
        get_header_for_element(p, 'h4'),
        get_header_for_element(p, 'h5'),
        get_header_for_element(p, 'h6'),
        p.text
    )
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
