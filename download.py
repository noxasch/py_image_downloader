"""
1. open up webpages using requests
2. convert into lxml object
3. Get list of image from xpath - input xpath
4. save image  - input save path
"""
import requests
import os
import sys
from requests.adapters import HTTPAdapter
from urllib.parse import urlparse, urljoin
from urllib3.util.retry import Retry
from time import sleep
from lxml import html
from os.path import dirname
from selenium import webdriver

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
    # print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    print(f'\r{prefix} |{bar}| {percent} {suffix}', end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def chrome_image_download(url, filename):
    browser = None
    try:
        options = webdriver.ChromeOptions()
        options.arguments.extend(['no-sandbox', 'disable-gpu'])
        browser = webdriver.Chrome(options=options)
        browser.get(url)
        el = browser.find_element_by_xpath("//img")
        if not el:
            raise Exception("No image found")
        el.click()
        # use headless and resize to the max height and width
        # cannot be done without headless
        # https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver
        with open(filename, 'wb') as f:
            f.write(el.screenshot_as_png)
        return browser.page_source
    except Exception as err:
        print(err)
    finally:
        if browser:
            if browser.session_id:
                browser.quit()


def save_file(folder, filename, resp):
    if not os.path.isdir(folder) and not os.path.exists(folder):
        os.makedirs(folder)
    count = 1  # to rename file if already exist
    while os.path.exists(f"{folder}/{filename}"):
        filename = f"({count})_{filename}"
        count += 1
    with open(f"{folder}/{filename}", 'wb') as f:
        f.write(resp._content)
    # return count + 1


def init_session():
    driver = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=1,
                    status_forcelist=[500, 502, 503, 504])
    driver.mount('http://', HTTPAdapter(max_retries=retries))
    return driver


def get_image_links(response, el_xpath):
    doc = html.fromstring(response.text)
    links = doc.xpath(el_xpath)
    print(f"{len(links)} image found")
    return links


def main(url, image_xpath, folder):
    print(f"{url}   {image_xpath}   {folder}")
    driver = init_session()
    response = driver.get(url, timeout=45)
    links = get_image_links(response,
                            image_xpath)  # default is None
    base_url = os.path.dirname(url)
    l = len(links)
    if l == 0:
        print(f"{l} links found, terminated.")
        exit()
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, item in enumerate(links):
        filename = str(item).split('/')[-1]
        item_url = urljoin(base_url, item)

        while True:
            try:
                response = driver.get(url=item_url, timeout=45)
                break
            except Exception as err:
                print(err)
            
        save_file(folder, filename, response)
        sleep(30)
        printProgressBar(i + 1, l, prefix='Progress:',
                         suffix='Complete', length=50)


if __name__ == "__main__":
    # args: filename url xpath outputFolder
    # python app_copy.py http://quantum.spline.one/ecommerce.html "//img[@class='img-fluid']/@src" spline_test
    url = sys.argv[1]
    image_xpath = sys.argv[2]
    folder = sys.argv[3]
    main(url, image_xpath, folder)
