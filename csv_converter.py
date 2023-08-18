import csv
import logging
from typing import NamedTuple, List, Tuple
from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)


class HeaderSection(NamedTuple):
    """Represents a section of content under specific headers."""
    h1: str
    h2: str
    h3: str
    h4: str
    h5: str
    h6: str
    content: str


def get_parent_header(t: Tag, header_name: str, prev_header_line: int, default_value: str = '') -> Tuple[str, int]:
    """
    Returns the header text for the tag and its line number
    or default_value and the previous header's line number.
    """
    header = t.find_previous_sibling(header_name)
    if header and header.sourceline > prev_header_line:
        return header.text, header.sourceline
    else:
        return default_value, prev_header_line


def not_a_header(t: Tag) -> bool:
    """Determines if a tag is not a header."""
    return t.name not in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def convert_html_to_csv(html_doc: str) -> List[HeaderSection]:
    """Converts an HTML document to a list of HeaderSection objects."""
    soup = BeautifulSoup(html_doc, 'html.parser')
    rows = []

    def get_headers(tag: Tag, prev_header_line: int = 0) -> Tuple[str, str, str, str, str, str, int]:
        """Retrieves the headers for a given tag."""
        headers = []
        for header_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            header_text, prev_header_line = get_parent_header(tag, header_name, prev_header_line)
            headers.append(header_text)
        return tuple(headers), prev_header_line

    def combine_rows_if_needed(rows: List[HeaderSection], headers: Tuple[str, str, str, str, str, str], tag_text: str) -> bool:
        """Combines rows if the headers match the previous row."""
        if rows and rows[-1][:-1] == headers:
            rows[-1] = rows[-1]._replace(content=rows[-1].content + '\n' + tag_text)
            return True
        return False

    for tag in soup.find_all(not_a_header, recursive=False):
        line = 0
        headers, line = get_headers(tag, line)
        if combine_rows_if_needed(rows, headers, tag.text):
            continue
        row = HeaderSection(*headers, tag.text)
        rows.append(row)

    return rows


def write_csv(rows: List[HeaderSection], csv_file_name: str) -> None:
    """Writes the HeaderSection objects to a CSV file."""
    logger.debug('Writing %d rows result to %s', len(rows), csv_file_name)
    with open(csv_file_name, 'w') as f:
        w = csv.writer(f)
        header_row = HeaderSection('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'content')
        w.writerow(header_row)
        w.writerows(rows)
