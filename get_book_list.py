"""Main method conducting the whole ETL process."""
import argparse
import parser_utils
import extract
import transform
import export
# import manage_db

def main():
    arg_parser = argparse.ArgumentParser(
        description="Get list of books from GoodReads.com and export them to a CSV file. Use -s to specify the shelf: -s non-fiction"
    )

    arg_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Will scrape limited number of books and will pause for the GoodRead captcha."
    )
    arg_parser.add_argument(
        "-s",
        "--shelf",
        type=str,
        help="Provide the name of the target Goodreads shelf, in order to know what book list to scrape."
    )
    args = arg_parser.parse_args()
    debug = args.debug
    shelf = args.shelf
    if debug:
        print("""
              Note: debug arg passed. The script will parse only a limited number of books and will
              pause at the Goodread capcha. Please solve the captcha if one appears and enter "continue"
              in the script in order to continue the process.
        """)

    print(f"debug: {debug}, shelf: {shelf}")
    

    # Get data, clean and transform it
    driver = parser_utils.selenium_request(debug)
    book_list = extract.extract_data(driver, debug, shelf)
    clean_book_list = transform.clean(book_list)
    driver.quit()

    # Generate CSV report
    export.generate_report(shelf, clean_book_list)

    # # Load data to a database
    # manage_db.init_db()
    # manage_db.load_books_into_db(clean_book_list)

if __name__ == '__main__':
    main()
