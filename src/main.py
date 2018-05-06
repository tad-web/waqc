from html_parser import HTMLParser


if __name__ == '__main__':
  url = 'http://www.tumblr.com'
  html_parser = HTMLParser([url])
  form_tags = html_parser.get_form_tags(url)
  form_notices = html_parser.get_bad_form_label_notices(url)
  print(form_notices)
  for form in form_notices:
      print(form)
  # [print(form.prettify(), "\n") for form in form_tags]
