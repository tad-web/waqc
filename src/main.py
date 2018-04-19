from html_parser import HTMLParser


if __name__ == '__main__':
    url = 'http://www.olin.edu/'
    html_parser = HTMLParser(url)
    print(html_parser.soup.prettify().splitlines())
    # for notice in html_parser.waqc():
    #    print(notice.line_num, notice.tag)
