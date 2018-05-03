from html_parser import HTMLParser


if __name__ == '__main__':
  url = 'https://www.carroll.org'
  html_parser = HTMLParser(url)
  url_notices = html_parser.run()
  print(url_notices)
