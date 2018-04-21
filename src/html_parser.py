import os
import requests
from bs4 import BeautifulSoup

from accessibility_notice import AccessibilityNotice
from enums import Flavor, Severity


class HTMLParser:
    def __init__(self, url, config_path='../config/'):
        self.config_path = config_path

        r = requests.get(url)
        html = str(r.content)
        self.soup = BeautifulSoup(html, 'html.parser')
        self.bad_link_names = self.txt_to_array('bad_link_names.txt')
        
    def txt_to_array(self, filename):
        curr_dir = os.path.dirname(__file__)
        path = curr_dir + '/' + self.config_path + filename
        with open(path, 'r') as f:
            lines = f.read()
            array = lines.splitlines()
            f.close()
        return array

    def write(self, filename):
        with open(filename, 'w') as f:
            f.write(self.soup.prettify())
            f.close()

    def get_links(self):
        return self.soup.find_all('a')

    def get_img_tags(self):
        return self.soup.find_all('img')

    def get_bad_link_label_tags(self):
        bad_link_tags = []
        for link in self.get_links():
            if (link.text.lower() in self.bad_link_names):
                bad_link_tags.append(link)
        return bad_link_tags

    def get_bad_alt_text(self):
        bad_img_tags = []
        for img_tag in self.get_img_tags():
            alt_text = img_tag['alt']
            if (alt_text == '' or alt_text.lower().endswith(('png', 'jpg'))):
                bad_img_tags.append(img_tag)
        return bad_img_tags

    def waqc(self):
        notices = []
        for tag in self.get_bad_link_label_tags():
            notices.append(AccessibilityNotice(tag, Flavor.LINK_LABEL, Severity.ERROR))
        for tag in self.get_bad_alt_text():
            notices.append(AccessibilityNotice(tag, Flavor.ALT_TEXT, Severity.ERROR))
        return notices
