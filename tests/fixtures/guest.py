import pytest

from rfidsecuritysvc.model.guest import Guest


@pytest.fixture(scope='session')
def guests(default_sound):
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Guest(1, 'Mickey', 'Mouse', default_sound.id, default_sound.name, 0xFFFFFF),
        Guest(2, 'Minnie', 'Mouse', default_sound.id, default_sound.name, 0xFFFFFF),
        Guest(3, 'Donald', 'Duck', default_sound.id, default_sound.name, 0xFFFFFF),
        Guest(4, 'Daisy', 'Duck', default_sound.id, default_sound.name, 0xFFFFFF),
        Guest(5, 'Dippy', 'Dawg', default_sound.id, default_sound.name, 0xFFFFFF),
        Guest(6, 'Princess', 'Anna', default_sound.id, default_sound.name, 0xFFFFFF),
    ]


@pytest.fixture(scope='session')
def creatable_guest(guests, default_sound):
    return Guest(len(guests) + 1, 'New', 'Guest', default_sound.id, default_sound.name, 0xFFFFFF)


@pytest.fixture(scope='session')
def not_authorized_media_guest(guests):
    return guests[4]


@pytest.fixture(scope='session')
def open_door_guest(guests):
    return guests[0]


@pytest.fixture(scope='session')
def guest_for_creatable_guest_media(guests):
    """ This guest should be used when creating a guest_media record."""
    return guests[0]


@pytest.fixture(scope='session')
def no_prefs_media_guest(guests):
    """ For use when building GuestMedia records """
    # Use Anna
    return guests[5]


@pytest.fixture(autouse=True, scope='session')
def add_guest_helpers(monkeypatch_session):
    def convert(self):
        copy = self.__dict__.copy()
        del copy['id']
        del copy['default_sound_name']
        del copy['default_color_hex']
        del copy['default_color_html']
        return copy

    monkeypatch_session.setattr(Guest, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Guest, 'test_update', convert, raising=False)
