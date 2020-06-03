from bs4 import BeautifulSoup
import requests
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

class MakeClass:
    def __init__(self, soup, fn):
        self.soup = soup
        self.fn = fn

    def get_name(self):
        div = self.soup.find("div", class_="page-title")
        self.name = div.get_text()

    def get_content(self):
        self.content = str(self.soup.find("div", id="page-content")).replace('"',"'")
    
    def make_class(self):
        self.get_name()
        self.get_content()

    def write_class(self):
        with open(self.fn, "a", encoding="UTF-16") as handle:
            handle.write('"{}","{}"\n'.format(self.name, self.content))
            handle.close()

        print("Got {}".format(self.name))


class ClassScraper:
    def __init__(self, fn):
        self.urls = []
        self.fn = fn
        self.list = ['Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard']
    
    def get_class_urls(self):
        for c in self.list:
            self.urls.append('http://dnd5e.wikidot.com/{}'.format(c.lower()))

    def get_soup(self, page):
        return BeautifulSoup(page, "lxml")  

    def get_classes(self):
        self.get_class_urls()
        with FuturesSession() as session:
            futures = [session.get(c) for c in self.urls]
            for future in as_completed(futures):
                resp = future.result()
                soup = self.get_soup(resp.content)
                class_soup = soup
                if 'you want to access does not exist.' in soup.get_text():
                    continue

                _class = MakeClass(class_soup, self.fn)
                _class.make_class()
                _class.write_class()



if __name__ == '__main__':
    class_file = "./classes.csv"
    c_scraper = ClassScraper(class_file)
    c_scraper.get_classes()