from config import *

def generate_report(book_list):
    filename = "book_list.csv"
    filepath = REPORTS_PATH + filename
    book_list.to_csv(filepath)
    print(f"See saved report as { filepath }")
