"""empty message

Revision ID: 4d3a986f11b3
Revises: 7466ebad4389
Create Date: 2020-06-05 11:23:50.043515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d3a986f11b3'
down_revision = '7466ebad4389'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('spellbook_ibfk_2', 'spellbook', type_='foreignkey')
    op.drop_constraint('spellbook_ibfk_1', 'spellbook', type_='foreignkey')
    op.create_foreign_key(None, 'spellbook', 'character', ['char_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'spellbook', 'spell', ['spell_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'spellbook', type_='foreignkey')
    op.drop_constraint(None, 'spellbook', type_='foreignkey')
    op.create_foreign_key('spellbook_ibfk_1', 'spellbook', 'character', ['char_id'], ['id'])
    op.create_foreign_key('spellbook_ibfk_2', 'spellbook', 'spell', ['spell_id'], ['id'])
    # ### end Alembic commands ###
