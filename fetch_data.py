from bs4 import BeautifulSoup
import requests
import re
import csv

SHOWBAGS_URL = "https://www.eastershow.com.au/explore/showbags/"
NUM_PAGES = 52

SHOWBAG_DIV = "showbagsCard"
SHOWBAG_NAME_HEADING = "showbagsCard-product--name"
SHOWBAG_PRICE_SPAN = "showbagsCard-product--price"
SHOWBAG_VALUE_DIV = "showbagsCard-description-copy--included"  # retail value is in the last paragraph inside <strong> tags

PRICE_PATTERN = r"\d+(\.\d{2})?"


def extract_price(full_string):
    matched = re.search(PRICE_PATTERN, full_string)
    if matched:
        return float(matched.group())
    return None


def write_to_text(showbags_data, textfile="showbags.txt"):
    """
    Takes in a list of dictionaries containing showbag data and outputs it to a
    text file   
    """

    text_output = open(textfile, "w")

    for showbag in showbags_data:
        print(f"--- {showbag['name']} ---", file=text_output)
        print(f"Price: ${showbag['price']}", file=text_output)
        print(f"Total retail value: ${showbag['retail_value']}", file=text_output)
        print(f"Value to price ratio: {showbag['value_ratio']}", file=text_output)
        print(file=text_output)

    text_output.close()


def write_to_csv(showbags_data, csvfile="showbags.csv"):
    """
    Takes in a list of dictionaries containing showbag data and outputs it to a
    CSV file   
    """

    csv_output = open(csvfile, "w")
    fieldnames = ["name", "items", "retail_value", "price", "value_ratio"]
    writer = csv.DictWriter(csv_output, fieldnames=fieldnames)

    writer.writeheader()

    for showbag_row in showbags_data:
        writer.writerow(
            {
                "name": showbag_row["name"],
                "items": showbag_row["items"],
                "retail_value": showbag_row["retail_value"],
                "price": showbag_row["price"],
                "value_ratio": showbag_row["value_ratio"],
            }
        )

    csv_output.close()


def write_to_html(showbags_data, htmlfile="index.html"):
    """
    Takes in a list of dictionaries containing showbag data and outputs the HTML
    into one big HTML file.

    Work in progress
    """

    html_output = open(htmlfile, "w")

    for showbag in showbags_data:
        print(showbag["html"], file=html_output)

    html_output.close()


def fetch_data():
    showbags_data = []
    unique_showbags = set()

    for n in range(1, NUM_PAGES + 1):
        page = requests.get(f"{SHOWBAGS_URL}/?page={n}")
        soup = BeautifulSoup(page.content, "html.parser")

        showbags = soup.find_all("div", class_=SHOWBAG_DIV)

        for showbag in showbags:
            name_heading = showbag.find("h3", class_=SHOWBAG_NAME_HEADING)
            name = name_heading.text.strip()

            if name in unique_showbags:
                print(f"duplicate: {name}")
                continue
            unique_showbags.add(name)

            print(f"processing: {name}")

            price_span = showbag.find("span", class_=SHOWBAG_PRICE_SPAN)
            price = extract_price(price_span.text)

            value_div = showbag.find("div", class_=SHOWBAG_VALUE_DIV)
            item_paragraphs = showbag.find_all("p")[:-2]
            all_items = [el.text for el in item_paragraphs]
            if all_items[-1].startswith("*"):
                all_items.pop()

            total_value_strong = value_div.find("strong")
            total_value = extract_price(total_value_strong.text)

            if not total_value or not price:
                value_to_price_ratio = 0
            else:
                value_to_price_ratio = total_value / price

            showbag_data = {
                "name": name,
                "price": price,
                "retail_value": total_value,
                "value_ratio": value_to_price_ratio,
                "items": "\n".join(all_items),
                "html": showbag,
            }
            showbags_data.append(showbag_data)

    showbags_data.sort(key=lambda x: x["value_ratio"], reverse=True)

    return showbags_data


if __name__ == "__main__":
    showbags_data = fetch_data()
    write_to_csv(showbags_data)
    write_to_text(showbags_data)
    write_to_html(showbags_data)
