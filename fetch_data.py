from bs4 import BeautifulSoup
import requests
import re

SHOWBAGS_URL = "https://www.eastershow.com.au/explore/showbags/"

SHOWBAG_DIV = "showbagsCard-content"
SHOWBAG_NAME_HEADING = "showbagsCard-product--name"
SHOWBAG_PRICE_SPAN = "showbagsCard-product--price"
SHOWBAG_VALUE_DIV = "showbagsCard-description-copy--included" # retail value is in the last paragraph inside <strong> tags

PRICE_PATTERN = r"\d+(\.\d{2})?"

def extract_price(full_string):
    matched = re.search(PRICE_PATTERN, full_string)
    if matched:
        return float(matched.group())
    return None

showbags_data = []

for n in range(1, 51):
    page = requests.get(f"{SHOWBAGS_URL}/?page={n}")
    soup = BeautifulSoup(page.content, "html.parser")

    showbags = soup.find_all("div", class_=SHOWBAG_DIV)

    for showbag in showbags:
        name_heading = showbag.find("h3", class_=SHOWBAG_NAME_HEADING)
        print(f"processing: {name_heading.text}")

        price_span = showbag.find("span", class_=SHOWBAG_PRICE_SPAN)
        price = extract_price(price_span.text)

        value_div = showbag.find("div", class_=SHOWBAG_VALUE_DIV)
        total_value_strong = value_div.find("strong")
        total_value = extract_price(total_value_strong.text)

        if not total_value or not price:
            value_to_price_ratio = 0
        else:
            value_to_price_ratio = total_value / price

        showbag_data = {
            "name": name_heading.text,
            "price": price,
            "retail_value": total_value,
            "value_ratio": value_to_price_ratio,
            "html": showbag
        }
        showbags_data.append(showbag_data)

showbags_data.sort(key=lambda x: x["value_ratio"], reverse=True)

text_output = open("showbags.txt", "w")
    
for showbag in showbags_data:
    print(f"--- {showbag['name']} ---", file=text_output)
    print(f"Price: ${showbag['price']}", file=text_output)
    print(f"Total retail value: ${showbag['retail_value']}", file=text_output)
    print(f"Value to price ratio: {showbag['value_ratio']}", file=text_output)
    print(file=text_output)

text_output.close()

html_output = open("showbags.html", "w")

for showbag in showbags_data:
    print(showbag['html'], file=html_output)

html_output.close()