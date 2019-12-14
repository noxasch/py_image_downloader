"""
1. open up webpages using requests
2. convert into lxml object
3. Get list of image from xpath - input xpath
4. save image  - input save path
"""
import requests
from urllib.parse import urlparse, urljoin
from time import sleep
from lxml import html

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}


if __name__ == "__main__":
    response = requests.get(url="http://quantum.spline.one/ecommerce.html", headers=HEADERS)
    response.raise_for_status()
    doc = html.fromstring(response.text)
    elements = doc.xpath("//img[@class='img-fluid']/@src")
    print(len(elements))


