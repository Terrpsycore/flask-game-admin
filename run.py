import os.path as op

from flask_admin import Admin
from flask_admin.base import AdminIndexView

from app import app, db
from models import Character, CharacterItem, CharacterMove, Item, Location, build_sample_db
from views import CharacterView, CharacterItemView, CharacterMoveView, ItemView, LocationView


admin = Admin(app,
    name='game control',
    template_mode='bootstrap3',
    index_view=AdminIndexView(name='Home', url='/')
)

admin.add_views(
    CharacterView(Character, db.session),
    CharacterItemView(CharacterItem, db.session),
    CharacterMoveView(CharacterMove, db.session),
    ItemView(Item, db.session),
    LocationView(Location, db.session)
)

if __name__ == '__main__':
    app_dir = op.realpath(op.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not op.exists(database_path):
        build_sample_db()
    app.run()
