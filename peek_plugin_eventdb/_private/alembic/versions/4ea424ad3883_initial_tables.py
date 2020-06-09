"""initial tables

Peek Plugin Database Migration Script

Revision ID: 4ea424ad3883
Revises:
Create Date: 2020-05-24 14:18:31.113373

"""

# revision identifiers, used by Alembic.
revision = '4ea424ad3883'
down_revision = None
branch_labels = None
depends_on = None

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('EventDBModelSet',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('key', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('comment', sa.String(), nullable=True),
                    sa.Column('propsJson', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('key'),
                    sa.UniqueConstraint('name'),
                    schema='pl_eventdb'
                    )
    op.create_table('Setting',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=50), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    schema='pl_eventdb'
                    )
    op.create_table('EventDBEvent',
                    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
                    sa.Column('dateTime', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('value', postgresql.JSONB(astext_type=sa.Text()),
                              nullable=False),
                    sa.Column('key', sa.String(), nullable=True),
                    sa.Column('modelSetId', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['modelSetId'],
                                            ['pl_eventdb.EventDBModelSet.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id', 'dateTime'),
                    schema='pl_eventdb'
                    )
    op.create_table('EventDBProperty',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('modelSetId', sa.Integer(), nullable=False),
                    sa.Column('key', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('order', sa.Integer(), nullable=False),
                    sa.Column('comment', sa.String(), nullable=True),
                    sa.Column('useForFilter', sa.Boolean(), nullable=True),
                    sa.Column('useForDisplay', sa.Boolean(), nullable=True),
                    sa.Column('displayByDefaultOnSummaryView', sa.Boolean(),
                              nullable=True),
                    sa.Column('displayByDefaultOnDetailView', sa.Boolean(),
                              nullable=True),
                    sa.Column('showFilterAs', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['modelSetId'],
                                            ['pl_eventdb.EventDBModelSet.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='pl_eventdb'
                    )
    op.create_index('idx_EventDBProp_name', 'EventDBProperty', ['modelSetId', 'key'],
                    unique=True, schema='pl_eventdb')
    op.create_index('idx_EventDBProp_value', 'EventDBProperty', ['modelSetId', 'name'],
                    unique=True, schema='pl_eventdb')
    op.create_table('SettingProperty',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('settingId', sa.Integer(), nullable=False),
                    sa.Column('key', sa.String(length=50), nullable=False),
                    sa.Column('type', sa.String(length=16), nullable=True),
                    sa.Column('int_value', sa.Integer(), nullable=True),
                    sa.Column('char_value', sa.String(length=50), nullable=True),
                    sa.Column('boolean_value', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['settingId'], ['pl_eventdb.Setting.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    schema='pl_eventdb'
                    )
    op.create_index('idx_SettingProperty_settingId', 'SettingProperty', ['settingId'],
                    unique=False, schema='pl_eventdb')
    op.create_table('EventDBPropertyValue',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('value', sa.String(), nullable=False),
                    sa.Column('comment', sa.String(), nullable=True),
                    sa.Column('propertyId', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['propertyId'],
                                            ['pl_eventdb.EventDBProperty.id'],
                                            ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    schema='pl_eventdb'
                    )
    op.create_index('idx_EventDBPropVal_name', 'EventDBPropertyValue',
                    ['propertyId', 'name'], unique=True, schema='pl_eventdb')
    op.create_index('idx_EventDBPropVal_value', 'EventDBPropertyValue',
                    ['propertyId', 'value'], unique=True, schema='pl_eventdb')
    # ### end Alembic commands ###

    # Convert the table to a timescale table
    # https://docs.timescale.com/latest/api#create_hypertable
    sql = '''
        SELECT create_hypertable('pl_eventdb."EventDBEvent"', 'dateTime');
    '''

    op.execute(sql)

    op.create_index('idx_EventDBEvent_modelSetId_key', 'EventDBEvent',
                    ['modelSetId', 'key'],
                    unique=False, schema='pl_eventdb')


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_EventDBPropVal_value', table_name='EventDBPropertyValue',
                  schema='pl_eventdb')
    op.drop_index('idx_EventDBPropVal_name', table_name='EventDBPropertyValue',
                  schema='pl_eventdb')
    op.drop_table('EventDBPropertyValue', schema='pl_eventdb')
    op.drop_index('idx_SettingProperty_settingId', table_name='SettingProperty',
                  schema='pl_eventdb')
    op.drop_table('SettingProperty', schema='pl_eventdb')
    op.drop_index('idx_EventDBProp_value', table_name='EventDBProperty',
                  schema='pl_eventdb')
    op.drop_index('idx_EventDBProp_name', table_name='EventDBProperty',
                  schema='pl_eventdb')
    op.drop_table('EventDBProperty', schema='pl_eventdb')
    op.drop_index('idx_EventDBEvent_modelSetId', table_name='EventDBEvent',
                  schema='pl_eventdb')
    op.drop_index('idx_EventDBEvent_key', table_name='EventDBEvent', schema='pl_eventdb')
    op.drop_table('EventDBEvent', schema='pl_eventdb')
    op.drop_table('Setting', schema='pl_eventdb')
    op.drop_table('EventDBModelSet', schema='pl_eventdb')
    # ### end Alembic commands ###
