# showbags-value
Find out which Sydney Easter Show showbags are the most worth!

Details on showbags sourced from the [Easter Show website](https://www.eastershow.com.au/explore/showbags/).

- `showbags.txt` - text file for sorted showbags with price, retail value, and value to price ratio
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
4. Run script to generate `showbags.txt` and `index.html`
```
python fetch_data.py
```
