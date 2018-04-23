from html_parser import HTMLParser


if __name__ == '__main__':
    url = 'http://www.olin.edu/admission/'
    html_parser = HTMLParser(url)
    notices = html_parser.waqc()
    for notice in notices:
        print(notice.flavor, notice.tag)
