from selenium import webdriver

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


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}

URL = "http://quantum.spline.one/ecommerce.html"
