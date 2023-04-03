import lxml
import requests
from bs4 import BeautifulSoup
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")
SMTP_HOST = os.environ.get("SMTP_HOST")
TO_EMAIL = os.environ.get("TO_EMAIL")

AMAZON_URL = "https://www.amazon.com/ASUS-VivoBook-i7-1165G7-Fingerprint-S533EA-DH74/dp/B08KH4P5TL/ref=sr_1_23?crid=V8EYT9RWM3W&keywords=laptop&qid=1678364052&refinements=p_89%3AASUS%2Cp_n_feature_thirty-one_browse-bin%3A23716064011%2Cp_n_size_browse-bin%3A2242801011&rnid=2242797011&s=pc&sprefix=laptop%2Caps%2C274&sr=1-23&th=1"

headers = {
    "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

response = requests.get(url=AMAZON_URL, headers=headers)
amazon_web = response.text

soup = BeautifulSoup(amazon_web, "lxml")

product_title = soup.find(id="productTitle").getText().strip().encode('utf-8')
product_title_str = str(product_title)[2:-1]

whole_price = soup.find(class_="a-price-whole").getText()
price_fraction = soup.find(class_="a-price-fraction").getText()

total_price = float(f"{whole_price}{price_fraction}")

print(product_title_str)
print(total_price)
print(AMAZON_URL)

#--------------------Email Alert When Price Below Preset Value--------------------

BUY_PRICE = 699.99

if total_price < BUY_PRICE:
    email_content = (f"{product_title_str} is now ${total_price}\n{AMAZON_URL}")
    with smtplib.SMTP(SMTP_HOST) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=f"Subject:Amazon Price Alert!\n\n{email_content}")
