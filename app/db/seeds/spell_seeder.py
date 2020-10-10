from app.models.spell import Spell
from app.models._class import _Class
from app.models.spellclass import SpellClass
from app.utils.model_helpers import *
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
import csv


class SpellSeeder():

    def __init__(self, app):
        self.app = app

    def run(self):
        
        data = []
        with open('app/db/seeds/data/spells2.csv', encoding="utf-16") as handle:
            csv_reader = csv.reader(handle, delimiter="#", quotechar='"')
            with self.app.app_context():

                for i, row in enumerate(csv_reader):
                    if len(row) == 19:
                        name = row[0]
                        if kw_get_model(Spell, name=name):
                            kw_delete_model(Spell, name=name)

                        class_info = row[10:]
                        spell = Spell(*row[:10])
                        insert_model(spell)

                        for class_name in class_info:
                            if class_name:
                                _class = kw_get_model(_Class, name=class_name)
                                insert_model(SpellClass(_class, spell))

                        if i % 10 == 0:
                            print(f"{i}: created {name}!")


        
