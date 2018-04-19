import os
import requests
from bs4 import BeautifulSoup


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

    def get_bad_links(self):
        bad_links = []
        for link in self.get_links():
            if (link.text.lower() in self.bad_link_names):
                bad_links.append(link.string)
        return bad_links

    def examine_links(self):
        for link in self.get_links():
            print(link.text)
