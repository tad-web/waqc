import os
import requests
import re
import random
from bs4 import BeautifulSoup

from accessibility_notice import AccessibilityNotice
from enums import Flavor, Severity


class HTMLParser:
  def __init__(self, urls, config_path='../config/'):
    """ Takes in a list of URLs, adds each one to self.urls, and adds all of the corresponding Soup
    objects to self.soups. """
    self.urls = []
    self.soups = {}

    for url in urls:
      self.add_url(url)

    self.config_path = config_path
    self.bad_link_labels = self.txt_to_array('bad_link_labels.txt')
    self.edit_field_types = self.txt_to_array('edit_field_types.txt')
    self.skip_link_labels = self.txt_to_array('skip_link_labels.txt')

  def add_url(self, url):
    """ Add the specified url to self.urls and add the corresponding soup object to self.soups. """
    self.urls.append(url)
    r = requests.get(url)
    html = str(r.content)
    self.soups[url] = BeautifulSoup(html, 'html.parser')

  def txt_to_array(self, filename):
    """ Look for the specified filename in our config folder, parse it, and return the contents as
    an array. The file should be newline delimited. """
    curr_dir = os.path.dirname(__file__)
    path = curr_dir + '/' + self.config_path + filename
    with open(path, 'r') as f:
      lines = f.read()
      array = lines.splitlines()
      f.close()
    return array

  def remove_url_prefixes(self, url):
    """ Returns the specified URL with the 'http://' and 'www.' prefixes removed. """
    url = re.sub('(https?://)?(www\.)?', '', url)
    return url

  def remove_url_suffixes(self, url):
    """ Returns the specified URL with the '/' suffixes removed. """
    return re.match('(https?://)?(www\.)?[^/]*', url).group()

  def remove_url_affixes(self, url):
    """ Returns the specified URL with the prefixes and suffixes removed. """
    url = self.remove_url_prefixes(url)
    url = self.remove_url_suffixes(url)
    return url

  def get_absolute_link(self, url, link):
    """ Return the absolute version of the specified link. The URL to prepend to the link (in the
    case that the link is a relative link) must be specified. """
    if url.endswith('/'): url = url[:-1]
    if link.startswith('//'): link = 'http:' + link
    elif link.startswith('/'): link = self.remove_url_suffixes(url) + link
    return link

  def are_urls_equal(self, url_1, url_2):
    """ Return true if the two URLs are the same once their prefixes and ending '/' have been
    removed. """
    url_1 = self.remove_url_prefixes(url_1)
    if url_1.endswith('/'): url_1 = url_1[:-1]
    url_2 = self.remove_url_prefixes(url_2)
    if url_2.endswith('/'): url_2 = url_2[:-1]
    return url_1 == url_2


  def is_link_internal(self, url, link):
    """ Returns if a specified link is a subpage of the specified URL. A link is defined as internal
    if it begins with the homepage URL, but does not equal the homepage URL. The specified link can
    be absolute or relative. """
    if self.are_urls_equal(url, link): return False
    p = re.compile('^((//)?(https?://)?(www\.)?' + self.remove_url_affixes(url) + '|/[^/]).*$')
    return bool(p.match(link))

  def get_link_tags(self, url):
    """ Return a list of all of the link tags from the soup object that corresponds to the
    specified URL. """
    return self.soups[url].find_all('a')

  def get_internal_link_tags(self, url):
    """ Return a list of all of the internal link tags from the soup object that corresponds to
    the specified URL. """
    link_tags = [tag for tag in self.get_link_tags(url) if tag.get('href') is not None]
    return [link_tag for link_tag in link_tags if self.is_link_internal(url, link_tag.get('href'))]

  def get_internal_links(self, url):
    """ Return a list of all internal links from the soup object that corresponds to the specified
    URL. Modify the links from the tags by making them absolute, rather than relative, URLs. """
    internal_link_tags = self.get_internal_link_tags(url)
    internal_links = [self.get_absolute_link(url, tag.get('href')) for tag in internal_link_tags]
    return internal_links

  def add_random_internal_url(self, url):
    """ Call self.add_url() on one randomly selected link from a list of all internal links from
    the specified URL. """
    internal_links = [link for link in self.get_internal_links(url) if link not in self.urls]
    if internal_links:
      internal_link = random.choice(internal_links)
      self.add_url(internal_link)

  def get_img_tags(self, url):
    """ Return a list of all of the img tags from the soup object that corresponds to the
    specified URL. """
    return self.soups[url].find_all('img')

  def get_header_tags(self, url):
    """ Return a list of all of the header tags from the soup object that corresponds to the
    specified URL. """
    return self.soups[url].find_all(re.compile('^h[1-6]$'))

  def get_form_tags(self, url):
    """ Return a list of all the form tags from the soup object that corresponds to the
    specified URL. """
    return self.soups[url].find_all('form')

  def get_bad_link_label_notices(self, url):
    """ Return a list of AccessibilityNotices for all bad link labels for the specified URL. """
    bad_link_label_notices = []
    for link_tag in self.get_link_tags(url):
      if (link_tag.text.lower() in self.bad_link_labels):
        bad_link_label_notices.append(AccessibilityNotice(link_tag, Flavor.LINK_LABEL,
            Severity.WARNING, 'This link label is potentially not descriptive enough \
            without context.'))
    return bad_link_label_notices

    def get_skip_links(self, url):
      """Return whether or not we've identified a skip link within the html """
      skip_link_notice =  []
      for link_tag in self.get_link_tags(url):
        if (link_tag.text.lower() in self.skip_link_labels):
          skip_link_notice.append(AccessibilityNotice(link_tag, Flavor.SKIP_LINK,
          Severity.EXCELLENT, 'This skip link is very useful and accessible.'))
        if (len(self.skip_link_labels) == 0):
          skip_link_notice.append(AccessibilityNotice(link_tag, Flavor.SKIP_LINK,
          Severity.WARNING, "We didn't find a skip link. Please ensure you have a skip to main content button available, especially if you have a large navigation bar."))
      return skip_link_notice

  def get_bad_alt_text_notices(self, url):
    """ Return a list of AccessibilityNotices for all bad alt texts for the specified URL. """
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
    """ Return a list of AccessibilityNotices for all bad headers for the specified URL. """
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

  def get_bad_form_label_notices(self, url):
    """ Return a list of AccessibilityNotices for all bad forms for the specified URL. """
    bad_field_labels_notices = []
    f_tags = self.get_form_tags(url)
    # Dictionary where k:v is form id : list of inputs of text-like fields
    forms_inputs_dict = {form.get('id'):[field for field in form.find_all('input') if field.get('type', 'no type') in self.edit_field_types] for form in f_tags}
    # Dictionary where k:v is form id: list of labels of all things
    forms_labels_dict = {form.get('id'):[label.get('for') for label in form.find_all('label')] for form in f_tags}
    for input_field in forms_inputs_dict.items():
      for tag in input_field[1]:
        if not tag.get('aria-label'):
          if not tag.get('id') in forms_labels_dict[input_field[0]]:
            bad_field_labels_notices.append(AccessibilityNotice(tag, Flavor.FORM_LABEL, Severity.WARNING,
                'This form entry is not labeled. If it is visible, it should be labeled appropriately.'))
    return bad_field_labels_notices

  def get_navbar_tags(self, url):
    navbar_tags = []
    for navbar_tag in self.soups[url].find_all('ul'):
      if re.match('.*nav.*', str(navbar_tag.attrs)):
        navbar_tags.append(navbar_tag)
    for navbar_tag in self.soups[url].find_all('nav'):
      navbar_tags.append(navbar_tag)
    return navbar_tags

  def get_navbar_links(self, url):
    """ Return a list of all links found in navigational bars. """
    navbar_tags = self.get_navbar_tags(url)
    navbar_links = set()
    for navbar_tag in navbar_tags:
      for link_tag in navbar_tag.find_all('a'):
        link = link_tag.get('href')
        if link is not None and self.is_link_internal(url, link):
          navbar_links.add(self.get_absolute_link(url, link))
    navbar_links = list(navbar_links)
    navbar_links.sort(key=len)
    return navbar_links

  def run(self):
    """ Return AccessibilityNotices in a parsable form to be displayed with Flask. An example of
    the data structure returned by this function is as follows:
    {
      'https://www.carroll.org': {
        'Link Label': [AccessibilityNotice],
        'Alt Text': [AccessibilityNotice],
        'Header': [AccessibilityNotice, AccessibilityNotice]
      },
      'https://carroll.org/help/volunteer-your-time/': {
        'Link Label': [],
        'Alt Text': [AccessibilityNotice, AccessibilityNotice],
        'Header': [AccessibilityNotice]
      }
    }
    """
    # self.add_random_internal_url(self.urls[0])
    url_notices = {}
    for url in self.urls:
      notices = {}
      notices[str(Flavor.SKIP_LINK)] = self.get_skip_links(url)
      notices[str(Flavor.LINK_LABEL)] = self.get_bad_link_label_notices(url)
      notices[str(Flavor.ALT_TEXT)] = self.get_bad_alt_text_notices(url)
      notices[str(Flavor.HEADER)] = self.get_bad_header_notices(url)
      notices[str(Flavor.FORM_LABEL)] = self.get_bad_form_label_notices(url)
      url_notices[url] = notices
    return url_notices
