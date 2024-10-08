import re
import pandas as pd
import config

def main():
    with open(config.PRIZES_FILEPATH + config.PULITZER_RAW_FILENAME, "r", encoding="utf-8") as file:
        lines = file.readlines()

    data = []
    for i, line in enumerate(lines):
        line = line.strip()

        if re.match(r"^\d{4}$", line):
            current_year = line
        elif "Pulitzer Prize for" in line:
            title = lines[i-1].strip()
            author_line = lines[i+1].strip()
            split_author_line = re.split(r"\s+by\s+", author_line)
            author = split_author_line[-1]
            category = line.replace("Pulitzer Prize for ", "").replace(":", "")

            data.append({
                "Year": current_year,
                "Category": category,
                "Title": title,
                "Author": author
            })

    df = pd.DataFrame(data)

    filepath = config.PRIZES_FILEPATH + config.PULITZER_CLEAN_FILENAME
    df.to_csv(filepath)


if __name__ == '__main__':
    main()
