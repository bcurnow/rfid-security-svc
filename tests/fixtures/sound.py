import os
from datetime import datetime
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
            Sound(1, 'test1.wav', datetime.now().isoformat(timespec='seconds'), wav_content),
            Sound(2, 'test2.wav', datetime.now().isoformat(timespec='seconds'), wav_content),
           ]


@pytest.fixture(scope='session')
def creatable_sound(sounds, wav_content):
    return Sound(len(sounds) + 1, 'creatable.wav', None, wav_content)


@pytest.fixture(scope='session')
def to_content():
    def _content(m, content_type='audio/wav'):
        fs = FileStorage(BytesIO(m.content), 'local file name.wav', m.name, content_type, len(m.content))
        return {'name': m.name, 'content': fs}
    return _content
