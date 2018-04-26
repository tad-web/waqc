from html_parser import HTMLParser


if __name__ == '__main__':
    url = 'http://www.olin.edu/admission/'
    html_parser = HTMLParser(url)
    notices_dict = html_parser.waqc()
    for notice_type in notices_dict:
      print(notice_type)
      for notice in notices_dict[notice_type]:
        print(notice.tag)
        print(notice.explanation)
