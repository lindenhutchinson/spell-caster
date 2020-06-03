# import things
from flask_table import Table, Col, BoolCol, LinkCol
from flask import url_for
# Declare your table
class SpellTable(Table):
    classes = ['spell-table']
    html_attrs = {'id':'spell-table-id'}
    name = LinkCol('Name', 'view_spell', url_kwargs=dict(id='id'), attr_list='name')
    level = Col('Level')
    concentration = BoolCol('Concentration')
    cast_time = Col('Cast Time')
    spell_range = Col('Range')
    duration = Col('Duration')
    school = Col('School')

    
