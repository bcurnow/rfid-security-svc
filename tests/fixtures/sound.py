import io
import os
import pytest
from _pytest.monkeypatch import MonkeyPatch
from rfidsecuritysvc.model.sound import Sound

@pytest.fixture(scope='session')
def wav_content() -> bytes:
    test_wav = os.path.join(os.path.dirname(__file__), 'test.wav')
    with open(test_wav, 'rb') as f:
        return f.read()


@pytest.fixture(scope='session')
def sounds(wav_content: bytes) -> list[Sound]:
    from rfidsecuritysvc.model.sound import Sound

    return [
        Sound(1, 'test1.wav', '2021-09-25 23:13:25', wav_content),
        Sound(2, 'test2.wav', '2021-09-25 23:13:25', wav_content),
    ]


@pytest.fixture(scope='session')
def creatable_sound(sounds: list[Sound], wav_content: bytes) -> Sound:
    from rfidsecuritysvc.model.sound import Sound

    return Sound(len(sounds) + 1, 'creatable.wav', '2021-09-25 23:13:25', wav_content)


@pytest.fixture(scope='session')
def default_sound(sounds: list[Sound]) -> Sound:
    return sounds[0]


@pytest.fixture(autouse=True, scope='session')
def add_sound_helpers(monkeypatch_session: MonkeyPatch) -> None:
    from rfidsecuritysvc.model.sound import Sound

    def convert(self):
        # Can't use eithe of the existing to_json methods as one doesn't contain
        # content and the other base64 encodes it
        copy = self.__dict__.copy()
        del copy['id']
        del copy['last_update_timestamp']
        return copy

    def test_to_row(self):
        copy = self.__dict__.copy()
        return copy

    def test_to_multipart(self, content_type='audio/wav'):
        # For multipart data, we need to return a tuple because this will need to be separated into form data (the first item)
        # and files (the second item)
        return (
            {
                'name': self.name,
            },
            {'content': (self.name, io.BytesIO(self.content), content_type)},
        )

    monkeypatch_session.setattr(Sound, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(Sound, 'test_update', convert, raising=False)
    monkeypatch_session.setattr(Sound, 'test_to_row', test_to_row, raising=False)
    monkeypatch_session.setattr(Sound, 'test_to_multipart', test_to_multipart, raising=False)
