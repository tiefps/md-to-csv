import csv
import logging
from typing import NamedTuple, List

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class ParagraphRow(NamedTuple):
    h1: str
    h2: str
    h3: str
    h4: str
    h5: str
    h6: str
    p: str


def get_parent_header(t: Tag, header_name: str, previous_header_line: int, default_value='') -> (str, int):
    """
    Returns the header text for the tag and its line number
    or default_value and the previous header's line number
    """
    header = t.find_previous_sibling(header_name)
    if header and header.sourceline > previous_header_line:
        return header.text, header.sourceline
    else:
        return default_value, previous_header_line


def not_a_header(t: Tag) -> bool:
    return t.name not in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def convert_html_to_csv(html_doc: str) -> List[ParagraphRow]:
    soup = BeautifulSoup(html_doc, 'html.parser')
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

    return rows


def write_csv(rows: List[ParagraphRow], csv_file_name: str):
    logger.debug('Writing %d rows result to %s', len(rows), csv_file_name)
    with open(csv_file_name, 'w') as f:
        w = csv.writer(f)
        header_row = ParagraphRow('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p')
        w.writerow(header_row)
        w.writerows(rows)
