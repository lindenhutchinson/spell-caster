from bs4 import BeautifulSoup
import requests
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import re

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
        with open(self.fn, "a", encoding="UTF-8") as handle:
            handle.write('"{}","{}"\n'.format(self.name, self.content))
            handle.close()

        print("Got {}".format(self.name))


class MakeSpell:
    def __init__(self, spell_soup, filename):
        self.soup = spell_soup
        self.data = [s.get_text() for s in self.soup.find_all("p")]
        self.fn = filename
        self.class_list = []

    def get_level_school(self):
        if 'cantrip' in self.data[0]:
            self.level = 0
            self.school = self.data[0].split(' ')[0].title()
        else:
            try:
                self.level = re.findall(r'(\d)', self.data[0])[0]
            except:
                self.level = 0

            self.school = self.data[0].split(' ')[-1].title()

    def get_info(self):
        rows = self.data[1].split('\n')
        items = []
        for row in rows:
            item = row.split(':')[1]
            items.append(item)

        self.cast_time = items[0]
        self.range = items[1]
        self.components = items[2]
        self.duration = items[3]

    def get_text(self):
        rows = self.data[2:-1]
        self.text = '\n'.join(rows)

    def get_name(self):
        div = self.soup.find("div", class_="page-title")
        self.name = div.get_text()

    def get_classes(self):
        row = self.data[-1]
        for c in ['Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard']:
            self.class_list.append(1 if c in row else 0)


    def write_spell(self):
        with open(self.fn, "a", encoding="UTF-8") as handle:
            handle.write('"{}",{},"{}","{}","{}","{}","{}", "{}", {}, {}, {}, {}, {}, {}, {}, {}\n'.format(
                self.name, self.level, self.school, self.cast_time, self.range, self.components, self.duration, self.text, *self.class_list))

            handle.close()

        print("Got {}".format(self.name))


    def make_spell(self):
        self.get_level_school()
        self.get_name()
        self.get_text()
        self.get_info()
        self.get_classes()


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

class SpellScraper:
    def __init__(self, url, file):
        self.base_url = url
        self.file = file
        self.spell_urls = []

    def get_soup(self, page):
        return BeautifulSoup(page, "lxml")

    def get_spell_urls(self):
        page = requests.get(url).content
        soup = self.get_soup(page)
        levels = soup.find_all("div", class_="feature")
        for spells in levels:
            spells = spells.find_all("a", href=True)
            for spell in spells:
                self.spell_urls.append(spell['href'])

        print("Found {} spells".format(len(self.spell_urls)))

    def get_spells(self):
        self.get_spell_urls()
        with FuturesSession() as session:
            futures = [session.get(spell) for spell in self.spell_urls]
            for future in as_completed(futures):
                resp = future.result()
                soup = self.get_soup(resp.content)
                spell_soup = soup
                if 'you want to access does not exist.' in soup.get_text():
                    continue

                if 'Spell List' in soup.find("div", class_="page-title").get_text():
                    break

                spell = MakeSpell(spell_soup, self.file)
                spell.make_spell()
                spell.write_spell()


    def print_spell_urls(self):
        print(len(self.spell_urls))


url = "http://dnd5e.wikidot.com/spells"
file = "../data/test.csv"
class_file = "../data/classes.csv"


# scraper = SpellScraper(url, file)
# scraper.get_spells()

c_scraper = ClassScraper(class_file)
c_scraper.get_classes()


