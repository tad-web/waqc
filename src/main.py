from html_parser import HTMLParser


if __name__ == '__main__':
  url = 'https://www.carroll.org/'
  html_parser = HTMLParser([url])
  navbar_links = html_parser.get_navbar_links(url)
  for link in navbar_links:
    print(link)
