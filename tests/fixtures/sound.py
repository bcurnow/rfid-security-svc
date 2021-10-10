import os
from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage

from rfidsecuritysvc.model.sound import Sound


@pytest.fixture(scope='session')
def wav_content():
    test_wav = os.path.join(os.path.dirname(__file__), 'test.wav')
    with open(test_wav, 'rb') as f:
        return f.read()


@pytest.fixture(scope='session')
def sounds(wav_content):
    return [
            Sound(1, 'test1.wav', content=wav_content),
            Sound(2, 'test2.wav', content=wav_content),
           ]


@pytest.fixture(scope='session')
def creatable_sound(sounds, wav_content):
    return Sound(len(sounds) + 1, 'creatable.wav', content=wav_content)


@pytest.fixture(scope='session')
def default_sound(sounds):
    return sounds[0]


@pytest.fixture(scope='session')
def to_content():
    def _content(m, content_type='audio/wav'):
        fs = FileStorage(BytesIO(m.content), 'local file name.wav', m.name, content_type, len(m.content))
        return {'name': m.name, 'content': fs}
    return _content


@pytest.fixture(autouse=True, scope='session')
def add_sound_helpers(monkeypatch_session):
    def convert(self):
        copy = self.__dict__.copy()
        del copy['id']
        del copy['last_update_timestamp']
        return copy

    monkeypatch_session.setattr(Sound, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Sound, 'test_update', convert, raising=False)
