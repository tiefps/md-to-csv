import logging

import markdown
import pypandoc

logger = logging.getLogger(__name__)


def convert_markdown_to_html(file_path: str, parser: str = 'pypandoc') -> str:
    """
    Converts a Markdown file to HTML using the specified parser.
    :param file_path: Path to the Markdown file to be converted.
    :param parser: Markdown parser to use ('markdown' or 'pypandoc'). Default is 'pypandoc'.
    :return: HTML content as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        logging.debug('File contents: %s', content)

    logger.debug(f'Converting to HTML using {parser}')
    if parser == 'markdown':
        html_content = markdown.markdown(content)
    elif parser == 'pypandoc':
        html_content = pypandoc.convert_text(content, 'html', format='md')
    else:
        raise ValueError("Invalid parser. Choose 'markdown' or 'pypandoc'.")

    # Logging the HTML content with a border
    border = "=" * 50
    logger.debug('Generated HTML: \n%s\n%s\n%s', border, html_content, border)

    return html_content
