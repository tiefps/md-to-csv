import logging
from datetime import datetime

from logging_config import configure_logging
from arg_parser import parse_arguments
from markdown_parser import convert_markdown_to_html
from csv_converter import convert_html_to_csv, write_csv


def main():
    args = parse_arguments()
    configure_logging(args.verbose)

    logging.info(f"Converting {args.input} to HTML using {args.parser} parser")
    html_content = convert_markdown_to_html(args.input, args.parser)
    logging.info("Converting HTML to CSV")
    rows = convert_html_to_csv(html_content)
    csv_file_name = args.output or f'out.{datetime.now().replace(microsecond=0).isoformat()}.csv'
    logging.info("Writing CSV to %s", csv_file_name)
    write_csv(rows, csv_file_name)
    logging.info("Conversion complete.")


if __name__ == "__main__":
    main()
