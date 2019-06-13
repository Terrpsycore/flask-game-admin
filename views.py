from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import rules

from app import db
from models import Character, CharacterItem, CharacterMove, Item, Location


def generate_rules(enabled:list, disabled:list):
    ''' Returns list of enable\disable rules for views. '''
    
    form_edit_rules = [rules.FieldSet(enabled)]

    for field in disabled:
        disabled_field = CustomizableField(field, field_args={'disabled': True})
        form_edit_rules.append(disabled_field)

    return form_edit_rules


class CustomizableField(rules.Field):
    ''' Field object that accepts additional arguments. '''

    def __init__(self, field_name, render_field='lib.render_field', field_args={}):
        super(CustomizableField, self).__init__(field_name, render_field)
        self.extra_field_args = field_args

    def __call__(self, form, form_opts=None, field_args={}):
        field_args.update(self.extra_field_args)
        return super(CustomizableField, self).__call__(form, form_opts, field_args)


class MetaView(ModelView):

    create_modal = True


class CharacterView(MetaView):

    form_edit_rules = generate_rules(
        ['name', 'clan', 'frags', 'password', 'created', 'last_active'],
        ['item_slots', 'location_moves']
    )


class CharacterItemView(MetaView):

    form_choices = {
        'place': [
            ('bag', 'Рюкзак'),
            ('belt', 'Пояс'),
            ('vault', 'Хранилище')
        ]
    }

    form_edit_rules = generate_rules(
        ['uses', 'place'],
        ['character', 'item']
    )


class CharacterMoveView(MetaView):

    form_edit_rules = generate_rules(
        ['last_visited'],
        ['character', 'location']
    )


class LocationView(MetaView):

    form_edit_rules = generate_rules(
        ['name'],
        ['characters_moves']
    )


class ItemView(MetaView):

    form_edit_rules = generate_rules(
        ['name'],
        ['characters_carrying']
    )
