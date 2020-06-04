from app.models.spell import Spell
from app.models._class import _Class
from app.utils.model_helpers import insert_model, delete_model_by_name, get_model_by_name
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
import csv

class ClassSeeder():

    def __init__(self, app):
        self.app = app

    def run(self):
        with open('app/db/seeds/data/classes.csv', encoding="utf-8") as handle:
            csv_reader = csv.reader(handle, delimiter=',', quotechar='"')
            with self.app.app_context():

                for row in csv_reader:
                    name = row[0]
                    if get_model_by_name(_Class, name):
                        delete_model_by_name(_Class, name)
                    insert_model(_Class(*row))
                    print("inserted a class!")