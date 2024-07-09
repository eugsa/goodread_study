import re

def split_additional_text(row):
  additional_text_sep = "—"
  additional_text = row.additional_text
  additional_text = re.sub(r"\s+", "", additional_text)
  additional_text = additional_text.split(additional_text_sep)

  row['average_rating'] = additional_text[0]
  row['amount_rating'] = additional_text[1]
  row['publishing_year'] = additional_text[2]
  return row

def clean(book_list):
  book_list = book_list.apply(split_additional_text, axis=1)
  book_list = book_list.drop("additional_text", axis=1)

  book_list.average_rating = book_list.average_rating.str.replace(r"[a-zA-Z]", "", regex=True)
  book_list.average_rating = book_list.average_rating.astype("float")
  book_list.amount_rating = book_list.amount_rating.str.replace(r"[a-zA-Z,]", "", regex=True)
  book_list.amount_rating = book_list.amount_rating.astype("int")
  book_list.publishing_year = book_list.publishing_year.str.replace(r"[a-zA-Z]", "", regex=True)
  book_list.publishing_year = book_list.publishing_year.astype("int", errors='ignore')

  return book_list