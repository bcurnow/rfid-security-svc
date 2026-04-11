from secrets import token_urlsafe
from werkzeug.security import check_password_hash, generate_password_hash
from connexion.exceptions import OAuthProblem
import sys
from . import media_perm, guest_media, config as config_table
from .base_model import BaseModel
from .media_perm import MediaPerm
from .guest_media import GuestMedia
from .guest import Guest
from .sound import Sound
from .color import Color
from .media import Media
from typing import Self


API_KEY_CONFIG_KEY = 'ADMIN_API_KEY' 
API_KEY_SIZE = 64

class MediaConfig(BaseModel):
    def __init__(self: Self, media_perm: MediaPerm, guest: Guest, sound: Sound, color: Color) -> None:
        self.media = media_perm.media
        self.permission = media_perm.permission
        self.guest = guest
        self.sound = sound
        self.color = color

    def to_json(self: Self) -> str:
        copy = super().to_json()
        copy['media'] = self.media.to_json()
        copy['permission'] = self.permission.to_json()
        if self.guest is not None:
            copy['guest'] = self.guest.to_json()
        if self.sound is not None:
            copy['sound'] = self.sound.to_json()
        if self.color is not None:
            copy['color'] = self.color.to_json()
        return copy


def authorized(media_id: str, perm_name: str) -> MediaConfig:
    mp = media_perm.get_by_media_and_perm(media_id, perm_name)
    if not mp:
        return
    # See if the media is associated with a guest
    gm = guest_media.get_by_media(media_id)

    color = None
    guest = None
    sound = None
    if gm:
        color = _resolveColor(gm)
        guest = gm.guest
        sound = _resolveSound(gm)

    return MediaConfig(mp, guest, sound, color)

def generate_api_key() -> str:
    """Generates a new 512-bit secure token, hashes it and stores it in the config table, returns the unhashed value"""
    
    # Generate a 1024 bit token
    token = token_urlsafe(API_KEY_SIZE)

    config_table.replace(API_KEY_CONFIG_KEY, generate_password_hash(token))
    return token



def ensure_api_key() -> None:
    """Ensure the admin API key exists; generate one if missing."""

    api_key_entry = config_table.get(API_KEY_CONFIG_KEY)
    if api_key_entry is None:
        key = generate_api_key()
        _print_new_key_warning(key)


def verify_api_key(apikey: str, required_scopes=None) -> dict:
    """Verify API key - called by Connexion security handler."""
    if not apikey:
        raise OAuthProblem('Invalid authentication: ""')

    try:
        config_entry = config_table.get(API_KEY_CONFIG_KEY)
        if not config_entry:
            raise OAuthProblem('Invalid authentication: ""')

        if not check_password_hash(config_entry.value, apikey):
            raise OAuthProblem(f'Invalid authentication: "{apikey}"')

        return {'uid': 'Admin API Key'}
    except OAuthProblem:
        raise
    except Exception:
        raise OAuthProblem('Invalid authentication: ""')


def _print_new_key_warning(key):
    print('IMPORTANT:', file=sys.stderr)
    print('******************************************************************************', file=sys.stderr)
    print('Please record this value as it will not be printed again.\n', file=sys.stderr)
    print(f'API key: "{key}".', file=sys.stderr)
    print('******************************************************************************', file=sys.stderr)

def _resolveColor(gm: MediaConfig) -> Color:
    if gm.color:
        return gm.color
    # This can also be None but that's OK
    return gm.guest.color


def _resolveSound(gm: MediaConfig) -> Sound:
    if gm.sound:
        return gm.sound
    return gm.guest.sound

