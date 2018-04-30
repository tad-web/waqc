import os
import requests
import re
import random
from bs4 import BeautifulSoup

from accessibility_notice import AccessibilityNotice
from enums import Flavor, Severity


class HTMLParser:
  def __init__(self, url, config_path='../config/'):
    self.urls = []
    self.soups = {}

    self.add_url(url)
    self.config_path = config_path

    self.bad_link_labels = self.txt_to_array('bad_link_labels.txt')

  def add_url(self, url):
    self.urls.append(url)
    r = requests.get(url)
    html = str(r.content)
    self.soups[url] = BeautifulSoup(html, 'html.parser')

  def txt_to_array(self, filename):
    curr_dir = os.path.dirname(__file__)
    path = curr_dir + '/' + self.config_path + filename
    with open(path, 'r') as f:
      lines = f.read()
      array = lines.splitlines()
      f.close()
    return array

  def write(self, url, filename):
    with open(filename, 'w') as f:
      f.write(self.soups[url].prettify())
      f.close()

  def get_link_tags(self, url):
    return self.soups[url].find_all('a')

  def get_internal_link_tags(self, url):
    trimmed_url = re.sub('(https?://)?(www\.)?', '', url)
    link_tags = [tag for tag in self.get_link_tags(url) if tag.get('href') is not None]
    p = re.compile('^((//)?(https?://)?(www\.)?' + trimmed_url + '|/[^/]).*$')
    return [link for link in link_tags if p.match(link.get('href'))]

  def get_internal_links(self, url):
    internal_link_tags = self.get_internal_link_tags(url)
    internal_links = [tag.get('href') for tag in internal_link_tags]
    internal_links = ['http:' + link if link.startswith('//') else link for link in internal_links]
    internal_links = [url + link if link.startswith('/') else link for link in internal_links]
    return internal_links

  def add_random_internal_url(self, url):
    internal_links = [link for link in self.get_internal_links(url) if link not in self.urls]
    if internal_links:
      internal_link = random.choice(internal_links)
      self.add_url(internal_link)

  def get_img_tags(self, url):
    return self.soups[url].find_all('img')

  def get_header_tags(self, url):
    return self.soups[url].find_all(re.compile('^h[1-6]$'))

  def get_bad_link_label_notices(self, url):
    bad_link_label_notices = []
    for link_tag in self.get_link_tags(url):
      if (link_tag.text.lower() in self.bad_link_labels):
        bad_link_label_notices.append(AccessibilityNotice(link_tag, Flavor.LINK_LABEL,
            Severity.WARNING, 'This link label is potentially not descriptive enough \
            without context.'))
    return bad_link_label_notices

  def get_bad_alt_text_notices(self, url):
    bad_alt_text_notices = []
    for img_tag in self.get_img_tags(url):
      alt_text = img_tag.get('alt', '')
      if (alt_text == ''):
        bad_alt_text_notices.append(AccessibilityNotice(img_tag, Flavor.ALT_TEXT,
            Severity.ERROR, 'This img tag has no alt text.'))
      elif(alt_text.lower().endswith(('png', 'jpg'))):
        bad_alt_text_notices.append(AccessibilityNotice(img_tag, Flavor.ALT_TEXT,
            Severity.ERROR, 'This img tag has alt text that ends with ' + alt_text[-3:] + ' which \
            normally indicates alt text set as an image file name.'))
    return bad_alt_text_notices

  def get_bad_header_notices(self, url):
    bad_header_notices = []
    h_tags = self.get_header_tags(url)
    for i in range(len(h_tags)):
      if i == 0 and int(h_tags[i].name[1]) != 1:
        bad_header_notices.append(AccessibilityNotice(h_tags[i], Flavor.HEADER, Severity.ERROR,
            'This is the first header on the page, but is not an h1.'))
      else:
        curr_h = int(h_tags[i].name[1])
        prev_h = int(h_tags[i-1].name[1])
        h_diff = curr_h - prev_h
        if h_diff > 1:
          bad_header_notices.append(AccessibilityNotice(h_tags[i], Flavor.HEADER, Severity.ERROR,
              'This header tag skipped at least one heading level. It should be changed to an h' +
              str(prev_h+1) + ' header.'))
    return bad_header_notices

  def waqc(self):
    # TODO check if no subpages, check if got a repeated subpage
    self.add_random_internal_url(self.urls[0])
    url_notices = {}
    for url in self.urls:
      notices = {}
      notices[str(Flavor.LINK_LABEL)] = self.get_bad_link_label_notices(url)
      notices[str(Flavor.ALT_TEXT)] = self.get_bad_alt_text_notices(url)
      notices[str(Flavor.HEADER)] = self.get_bad_header_notices(url)
      url_notices[url] = notices
    return url_notices
