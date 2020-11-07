from secrets import token_urlsafe
from connexion.exceptions import OAuthProblem
from werkzeug.security import check_password_hash, generate_password_hash
from rfidsecuritysvc.model import config

API_KEY_CONFIG_KEY = 'ADMIN_API_KEY'

def generate_api_key():
    """Generates a new 512-bit secure token, hashes it and stores it in the config table, returns the unhashed value"""
    # Generate a 1024 token
    token = token_urlsafe(64)
    
    #Always delete first to avoid a duplicate key error
    config.delete(API_KEY_CONFIG_KEY)
    config.create(API_KEY_CONFIG_KEY, generate_password_hash(token))
    return token

def verify_apikey(apikey, required_scopes):
    if check_password_hash(config.get(API_KEY_CONFIG_KEY).value, apikey):
        return {'uid': 'Admin API Key'}
    raise OAuthProblem(f'Invalid authentication: "{apikey}"')


