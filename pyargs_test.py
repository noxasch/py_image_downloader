import sys, re

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Downloader:
    def __init__(self):
        print("Object initated")
        super().__init__()

    def __del__(self):
        print("object cleared")


if __name__ == "__main__":
    print(sys.argv) # include script name
    print(sys.argv[1:]) # exclude script name
    print(re.match(regex, sys.argv[1]) is not None)
    test = Downloader()
    print("test end...")
