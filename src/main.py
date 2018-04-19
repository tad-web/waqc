from html_parser import HTMLParser


if __name__ == '__main__':
    url = 'http://www.olin.edu/'
    html_parser = HTMLParser(url)
    print(html_parser.get_bad_links())
