from flask_seeder import Seeder, Faker, generator
from app.models.spell import Spell
from app.utils.model_helpers import insert_model, insert_seeded_model
from app.app import create_app, register_extensions
from app.config.config import DevelopmentConfig
import csv
# All seeders inherit from Seeder


class SpellSeeder():

    def __init__(self, app):
        self.app = app

    # run() will be called by Flask-Seeder
    def run(self):
        
        data = []
        with open('app/db/seeds/data/spells.csv') as handle:
            csv_reader = csv.reader(handle, delimiter='#')
            line_count = 0
            with self.app.app_context():

                for row in csv_reader:

                        insert_model(Spell(*row))
                        print("inserted a spell!")

        

                # else:
                #     print(
                #         f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                    # line_count += 1

            #     for d in read['spells']:
            #         print(d)
            #         break
            # insert_seeded_model(Spell, d.i)
            # print("got a spell")
            # print(d)
            # print('\n\n\n')
        # Create a new Faker and tell it how to create Class objects
        #     faker = Faker(
        #         cls=Spell,
        #         init=

        #     )

        # # Create 5 class
        #     for spell in faker.create(5):
        #         print("Adding spell: %s" % spell)
        #         insert_model(spell)
