from app.models.monster import Monster
from app.models._class import _Class
from app.utils.model_helpers import *
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
import csv


class MonsterSeeder():

    def __init__(self, app):
        self.app = app

    def run(self):
        
        data = []
        with open('app/db/seeds/data/monsters.csv', encoding="utf-8") as handle:
            csv_reader = csv.reader(handle, delimiter=",", quotechar='"')
            with self.app.app_context():

                for row in csv_reader:
                    name = row[0]
                    if kw_get_model(Monster, name=name):
                        kw_delete_model(Monster, name=name)

                    insert_model(Monster(*row))
                    print("inserted a monster!")


        
