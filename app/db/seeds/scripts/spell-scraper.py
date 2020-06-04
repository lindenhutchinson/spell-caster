from bs4 import BeautifulSoup
import requests
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import re
import time
import os


def clear(): return os.system('cls')


class Timer:
    def __init__(self, start, total):
        self.start = start
        self.total = total

    def get_download_speed(self, count):
        taken = time.time() - self.start
        sec_per_dl = taken / count
        return sec_per_dl

    def get_remaining_time(self, count):
        time_per_dl = self.get_download_speed(count)
        rem = self.total - count
        time_rem = time_per_dl * rem
        return time_rem

    def get_formatted_time(self, time):
        if time > 60:
            return "%s minutes" % round(time/60, 2)
        else:
            return "%s seconds" % round(time, 1)

    def print_progress(self, count):
        clear()
        rem_time = self.get_remaining_time(count)
        form_rem = self.get_formatted_time(rem_time)
        form_cur = self.get_formatted_time(time.time()-self.start)

        print("Est. %s remaining\nHave got %d/%d in %s!\n" %
              (form_rem, count, self.total, form_cur))
        print("Currently downloading 1 entry every %s\n" %
              (self.get_formatted_time(self.get_download_speed(count))))

    def finished(self, count):
        clear()
        print("It took %s to download %d spells!" %
              (self.get_formatted_time(time.time()-self.start), count))


class SpellScraper:
    def __init__(self, url, file):
        self.base_url = url
        self.file = file
        self.spell_urls = []

    def get_soup(self, page):
        return BeautifulSoup(page, "lxml")

    def get_spell_urls(self):
        page = requests.get(self.base_url).content
        soup = self.get_soup(page)
        spells = soup.find_all("a", class_="pull-right", href=True)

        for spell in spells:
            self.spell_urls.append(spell['href'])

        print("Found {} spells".format(len(self.spell_urls)))

    def get_spells(self):
        self.get_spell_urls()
        timer = Timer(time.time(), len(self.spell_urls))
        count = 0
        with FuturesSession() as session:
            futures = [session.get(spell) for spell in self.spell_urls]
            for future in as_completed(futures):
                resp = future.result()
                soup = self.get_soup(resp.content)
                spell_soup = soup

                spell = MakeSpell(spell_soup, self.file)
                spell.make_spell()
                spell.write_spell()
                count += 1
                timer.print_progress(count)



class MakeSpell:
    def __init__(self, spell_soup, filename):
        self.data = self.get_data(spell_soup)
        self.fn = filename
        self.class_list = []

    def get_data(self, soup):
        unclean = [s.get_text() for s in soup.find_all("p")]
        data = []
        for d in unclean:
            d = d.strip('\r\n ')
            d = d.replace('’', "'")
            if d == '':
                continue
            if 'Create and save your' in d:
                continue
            if 'Join our mailing list' in d:
                continue
            if 'Lots of you gamers think' in d:
                continue
            if 'Some rights might be Reserved' in d:
                continue
            if 'Wizards of the Coast' in d:
                continue
            if 'not affiliated with' in d:
                continue

            data.append(d)

        return data

    '''
    -school
    -level
    -cast time
    -range
    -components
    -duration 
    '''

    def get_info(self):
        self.school = self.data[1]
        rows = self.data[2].split('\r\n')
        items = []
        for row in rows:
            item = row.split(':')[1]
            items.append(item.strip(' \n'))

        self.level = 0 if items[0] == 'Cantrip' else items[0]
        self.cast_time = items[1]
        self.range = items[2]
        self.components = items[3]
        self.duration = items[4]
        self.concentration = 1 if 'Concentration' in self.duration else 0

    def get_text(self):
        self.text = self.data[3].replace('\n', '<br>').replace('\r', '')

    def get_level_scaling(self):
        scaling = self.data[4]
        self.scaling = scaling if 'When you cast this spell' in scaling else ' '

    def get_book(self):
        book = self.data[-2]
        self.book = book.split(':')[1].strip()

    def get_name(self):
        div = self.soup.find("h1", class_="classic-title")
        self.name = div.get_text()

    def get_classes(self):
        row = self.data[-1]
        for c in ['Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger', 'Sorcerer', 'Warlock', 'Wizard']:
            self.class_list.append(1 if c in row else 0)

    def write_spell(self):
        with open(self.fn, "a", encoding="UTF-16") as handle:
            handle.write('"{}"#{}#"{}"#"{}"#"{}"#"{}"#"{}"#"{}"#"{}"#"{}"#{}#{}#{}#{}#{}#{}#{}#{}#{}\n'.format(
                self.name, self.level, self.school, self.cast_time, self.range, self.components, self.duration, self.text, self.book, self.scaling, self.concentration, *self.class_list))

            handle.close()

    def make_spell(self):
        self.get_info()
        self.get_name()
        self.get_book()
        self.get_level_scaling()
        self.get_text()
        self.get_classes()


if __name__ == '__main__':
    url = "https://www.dnd-spells.com/spells"
    file = "./spells.csv"
    scraper = SpellScraper(url, file)
    scraper.get_spells()
