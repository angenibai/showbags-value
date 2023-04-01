# showbags-value
Find out which Sydney Easter Show showbags are the most worth!

Details on showbags sourced from the [Easter Show website](https://www.eastershow.com.au/explore/showbags/).

- `showbags.txt` - text file for sorted showbags with price, retail value, and value to price ratio
- `showbags.csv` - csv file for sorted showbags with items in the bag, price retail value, and value to price ratio
- `index.html` - html to view sorted showbags in the browser

## Running locally

1. Install pipenv
2. Install dependencies from pipfile
```
pipenv install
```
3. Launch environment
```
pipenv shell
```
4. Run script to generate `showbags.txt`, `showbags.csv`, and `index.html`
```
python fetch_data.py
```

### Editing variables 

`SHOWBAGS_URL` - the base URL for the showbags website. This could potentially change between years so double check it is still accurate.

`NUM_PAGES` - total number of pages on the showbags website. This is definitely prone to change so have a look before running the script.