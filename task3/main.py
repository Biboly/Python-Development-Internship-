import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.bloomberg.com/asia"

# Send a GET request to the URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

news_links = soup.find_all('a', href=True)

news_headlines = []

for link in news_links:
    href = link['href']
    text = link.get_text(strip=True)
    if '/news/articles/' in href and text:
        news_headlines.append((text, href))

df = pd.DataFrame(news_headlines, columns=['Headline', 'Link'])

df.to_csv('news_headlines.csv', index=False)