import pytest

from rfidsecuritysvc.model.guest import Guest


@pytest.fixture(scope='session')
def guests(default_sound):
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Guest(1, 'Mickey', 'Mouse', default_sound.id, 0xFFFFFF),
        Guest(2, 'Minnie', 'Mouse', default_sound.id, 0xFFFFFF),
        Guest(3, 'Donald', 'Duck', default_sound.id, 0xFFFFFF),
        Guest(4, 'Daisy', 'Duck', default_sound.id, 0xFFFFFF),
        Guest(5, 'Dippy', 'Dawg', default_sound.id, 0xFFFFFF),
        Guest(6, 'Princess', 'Anna', default_sound.id, 0xFFFFFF),
    ]


@pytest.fixture(scope='session')
def creatable_guest(guests, default_sound):
    return Guest(len(guests) + 1, 'New', 'Guest', default_sound.id, 0xFFFFFF)
