from secrets import token_urlsafe
from werkzeug.security import check_password_hash, generate_password_hash
from connexion.exceptions import OAuthProblem
import sys

from rfidsecuritysvc.model import config

API_KEY_CONFIG_KEY = 'ADMIN_API_KEY'
API_KEY_SIZE = 64


def generate_api_key() -> str:
    """Generates a new 512-bit secure token, hashes it and stores it in the config table, returns the unhashed value"""
    # Generate a 1024 bit token
    token = token_urlsafe(API_KEY_SIZE)

    config.replace(API_KEY_CONFIG_KEY, generate_password_hash(token))
    return token


def ensure_api_key() -> None:
    """Ensure the admin API key exists; generate one if missing."""
    from rfidsecuritysvc.db import config

    api_key_entry = config.get(API_KEY_CONFIG_KEY)
    if api_key_entry is None:
        key = generate_api_key()
        _print_new_key_warning(key)


def verify_apikey(apikey: str, required_scopes=None) -> dict:
    """Verify API key - called by Connexion security handler."""
    if not apikey:
        raise OAuthProblem('Invalid authentication: ""')

    try:
        config_entry = config.get(API_KEY_CONFIG_KEY)
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
    print("IMPORTANT:", file=sys.stderr)
    print("******************************************************************************", file=sys.stderr)
    print("Please record this value as it will not be printed again.\n", file=sys.stderr)
    print(f"API key: \"{key}\".", file=sys.stderr)
    print("******************************************************************************", file=sys.stderr)
