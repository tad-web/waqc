from html_parser import HTMLParser


if __name__ == '__main__':
  url = 'http://www.olin.edu/admission/'
  html_parser = HTMLParser(url)
  url_notices = html_parser.waqc()
  for url in url_notices:
    print(url)
    print(url_notices[url])
