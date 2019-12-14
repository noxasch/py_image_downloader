"""
1. open up webpages using requests
2. convert into lxml object
3. Get list of image from xpath - input xpath
4. save image  - input save path
"""
import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse, urljoin
from urllib3.util.retry import Retry
from time import sleep
from lxml import html
from os.path import dirname

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}

URL = "http://quantum.spline.one/ecommerce.html"


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()



if __name__ == "__main__":
    s = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    response = s.get(url=URL, timeout=45)
    doc = html.fromstring(response.text)
    elements = doc.xpath("//img[@class='img-fluid']/@src")
    print(len(elements))
    base_url = dirname(URL)
    print(base_url)
    l = len(elements)
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, item in enumerate(elements):
        printProgressBar(i + 1, l, prefix='Progress:',
                         suffix='Complete', length=50)
        filename = str(item).split('/')[-1] # grab the filename and extension
        item = urljoin(base_url, item)
        response = s.get(url=item, timeout=45)
        with open(f"spline/{filename}", 'wb') as f:
            f.write(response._content)
        sleep(2)
    print("test done")

