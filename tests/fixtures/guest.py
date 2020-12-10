import pytest

from rfidsecuritysvc.model.guest import Guest


@pytest.fixture(scope='session')
def guests():
    # The DB will return these ordered by id, please build the list accordingly
    return [
        Guest(1, 'Mickey', 'Mouse'),
        Guest(2, 'Minnie', 'Mouse'),
        Guest(3, 'Donald', 'Duck'),
        Guest(4, 'Daisy', 'Duck'),
        Guest(5, 'Dippy', 'Dawg'),
        Guest(6, 'Princess', 'Anna'),
    ]


@pytest.fixture(scope='session')
def creatable_guest(guests):
    return Guest(len(guests) + 1, 'New', 'Guest')


@pytest.fixture(scope='session')
def open_door_guest(guests):
    return guests[5]
