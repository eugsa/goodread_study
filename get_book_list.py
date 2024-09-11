"""Main method conducting the whole ETL process."""
import argparse
import parser_utils
import extract
import transform
import export
import manage_db

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

    # Get data, clean and transform it
    driver = parser_utils.selenium_request(debug)
    book_list = extract.extract_data(driver, debug)
    clean_book_list = transform.clean(book_list)
    driver.quit()

    # Generate CSV report
    export.generate_report(clean_book_list)

    # Load data to a database
    manage_db.init_db()
    manage_db.load_books_into_db(clean_book_list)

if __name__ == '__main__':
    main()
