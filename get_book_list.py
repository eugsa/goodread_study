"""Main method conducting the whole ETL process."""
import argparse
import parser_utils
import extract
import transform
import export

def main():
    arg_parser = argparse.ArgumentParser(
        description="Get list of books from GoodReads.com and export them to a CSV file."
    )

    arg_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Will scrape limited number of books and will pause for the GoodRead captcha."
    )
    args = arg_parser.parse_args()
    debug = args.debug
    if debug:
        print("""
              Note: debug arg passed. The script will parse only a limited number of books and will
              pause at the Goodread capcha. Please solve the captcha if one appears and enter "continue"
              in the script in order to continue the process.
        """)

    driver = parser_utils.selenium_request(debug)
    book_list = extract.extract_data(driver, debug)
    clean_book_list = transform.clean(book_list)
    export.generate_report(clean_book_list)
    driver.quit()

if __name__ == '__main__':
    main()
