import pytest

from rfidsecuritysvc.model.media_perm import MediaPerm


@pytest.fixture(scope='session')
def media_perms(media_for_permissions, open_door_media, open_door_permission, default_permission):
    # The DB will return these ordered by id, please build the list accordingly
    media_perms = []
    for i in range(len(media_for_permissions)):
        media_perms.append(MediaPerm(i + 1, media_for_permissions[i], default_permission))
    media_perms.append(MediaPerm(len(media_perms) + 1, open_door_media, open_door_permission))
    return media_perms


@pytest.fixture(scope='session')
def creatable_media_perm(media_perms, media_for_creatable_media_perm, permission_for_creatable_media_perm):
    return MediaPerm(len(media_perms) + 1, media_for_creatable_media_perm, permission_for_creatable_media_perm)


@pytest.fixture(scope='session')
def media_perm_to_row():
    def to_row(m):
        row = {}
        row['id'] = m.id
        row['media_id'] = m.media.id
        row['media_name'] = m.media.name
        row['media_desc'] = m.media.desc
        row['permission_id'] = m.permission.id
        row['permission_name'] = m.permission.name
        row['permission_desc'] = m.permission.desc
        return row

    return to_row


@pytest.fixture(autouse=True, scope='session')
def add_media_perm_helpers(monkeypatch_session):
    def convert(self):
        return {
            'media_id': self.media.id,
            'permission_id': self.permission.id,
        }

    monkeypatch_session.setattr(MediaPerm, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(MediaPerm, 'test_update', convert, raising=False)
