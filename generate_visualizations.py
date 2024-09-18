import os
import pandas as pd
import config

def visualize_data(nonfic_books_csv, dnf_books_csv):
    nonfic_df = pd.read_csv(nonfic_books_csv, index_col=0)
    dnf_df = pd.read_csv(dnf_books_csv, index_col=0)

    print(nonfic_df.head())
    print(nonfic_df.info())
    print(dnf_df.head())
    print(dnf_df.info())

def main():
    nonfic_books_csv = config.REPORTS_PATH + config.NONFIC_FILENAME
    dnf_books_csv = config.REPORTS_PATH + config.DNF_FILENAME

    if os.path.isfile(nonfic_books_csv) and os.path.isfile(dnf_books_csv):
        visualize_data(nonfic_books_csv, dnf_books_csv)
    else:
        print("""
              Please first scrape the data for non-fiction and dnf books
              with the get_book_data.py script.
        """)

if __name__ == '__main__':
    main()
