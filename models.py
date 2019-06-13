from datetime import datetime

from app import app, db


class Character(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    clan = db.Column(db.String(100), nullable=False)
    frags = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    last_active = db.Column(db.DateTime, nullable=False)

    item_slots = db.relationship('CharacterItem', lazy='select',
        backref=db.backref('character', lazy='joined'))
    location_moves = db.relationship('CharacterMove', lazy='select',
        backref=db.backref('character', lazy='joined'))

    def __str__(self):
        return self.name


class CharacterItem(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uses = db.Column(db.Integer, nullable=False, default=0)
    place = db.Column(db.String(20), nullable=False)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship("Item", uselist=False,
        backref=db.backref("characters_carrying", uselist=False))


class CharacterMove(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    last_visited = db.Column(db.DateTime, nullable=False)

    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    location = db.relationship("Location", uselist=False,
        backref=db.backref("characters_moves"))


class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __str__(self):
        return self.name


def build_sample_db():
    db.drop_all()
    db.create_all()

    character_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]

    for i in range(len(character_names)):
        character = Character(
            name = character_names[i],
            clan = i // 8,
            frags = 0,
            password = character_names[i][::-1],
            created = datetime.now(),
            last_active = datetime.now()
        )
        db.session.add(character)

        item = Item(
            name = "{}'s item".format(character_names[i])
        )
        db.session.add(item)

        location = Location(
            name = "{}'s home".format(character_names[i])
        )
        db.session.add(location)

        character_item = CharacterItem(
            uses = 0,
            place = 'bag',
            character = character,
            item = item
        )
        db.session.add(character_item)

        character_move = CharacterMove(
            last_visited = datetime.now(),
            character = character,
            location = location
        )
        db.session.add(character_move)

    db.session.commit()


if __name__ == '__main__':
    db.init_app(app)
    db.create_all(app=app)
