from app.models.spell import Spell
from app.models._class import _Class
from app.utils.model_helpers import insert_model, delete_model_by_name, get_model_by_name
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
                        name = row[0]
                        if kw_get_model(Spell, name=name):
                            kw_delete_model(Spell, name=name)

                        insert_model(Spell(*row))
                        print("inserted a spell!")


        
