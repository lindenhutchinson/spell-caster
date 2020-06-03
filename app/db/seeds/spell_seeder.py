from app.models.spell import Spell
from app.models._class import _Class
from app.utils.model_helpers import insert_model, insert_seeded_model
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
import csv


class SpellSeeder():

    def __init__(self, app):
        self.app = app

    def run(self):
        
        data = []
        with open('app/db/seeds/data/spells.csv', encoding="utf-16") as handle:
            csv_reader = csv.reader(handle, delimiter="#", quotechar='"')
            with self.app.app_context():

                for row in csv_reader:
                    if len(row) == 19:
                        
                        insert_model(Spell(*row))
                        print("inserted a spell!")

class ClassSeeder():

    def __init__(self, app):
        self.app = app

    def run(self):
        
        data = []
        with open('app/db/seeds/data/classes.csv', encoding="utf-16") as handle:
            csv_reader = csv.reader(handle, delimiter=',', quotechar="'")
            with self.app.app_context():

                for row in csv_reader:
                        insert_model(_Class(*row))
                        print("inserted a class!")
        
