import pytest

from rfidsecuritysvc.model.guest import Guest


@pytest.fixture(scope='session')
def guests(default_sound, default_color):
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Guest(1, 'Mickey', 'Mouse', default_sound, default_color),
        Guest(2, 'Minnie', 'Mouse', default_sound, default_color),
        Guest(3, 'Donald', 'Duck', default_sound, default_color),
        Guest(4, 'Daisy', 'Duck', default_sound, default_color),
        Guest(5, 'Dippy', 'Dawg', default_sound, default_color),
        Guest(6, 'Princess', 'Anna', default_sound, default_color),
        Guest(7, 'Princess', 'Else', default_sound, default_color),
    ]


@pytest.fixture(scope='session')
def creatable_guest(guests, default_sound, default_color):
    return Guest(len(guests) + 1, 'New', 'Guest', default_sound, default_color)


@pytest.fixture(scope='session')
def not_authorized_media_guest(guests):
    for g in guests:
        if g.first_name == 'Dippy' and g.last_name == 'Dawg':
            return g


@pytest.fixture(scope='session')
def open_door_guest(guests):
    for g in guests:
        if g.first_name == 'Mickey' and g.last_name == 'Mouse':
            return g


@pytest.fixture(scope='session')
def guest_for_creatable_guest_media(guests):
    """ This guest should be used when creating a guest_media record."""
    for g in guests:
        if g.first_name == 'Mickey' and g.last_name == 'Mouse':
            return g


@pytest.fixture(scope='session')
def no_prefs_media_guest(guests):
    """ For use when building GuestMedia records """
    for g in guests:
        if g.first_name == 'Princess' and g.last_name == 'Anna':
            return g


@pytest.fixture(autouse=True, scope='session')
def add_guest_helpers(monkeypatch_session):
    def convert(self):
        sound = None
        if self.sound:
            sound = self.sound.id

        color = None
        if self.color:
            color = self.color.int

        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'sound': sound,
            'color': color,
        }

    def to_row(self):
        row = {}
        row['id'] = self.id
        row['first_name'] = self.first_name
        row['last_name'] = self.last_name
        row['sound'] = self.sound.id
        row['sound_name'] = self.sound.name
        row['sound_last_update_timestamp'] = self.sound.last_update_timestamp
        row['color'] = self.color.int
        return row

    monkeypatch_session.setattr(Guest, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Guest, 'test_update', convert, raising=False)
    monkeypatch_session.setattr(Guest, 'test_to_row', to_row, raising=False)
