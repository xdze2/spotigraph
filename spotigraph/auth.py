
import tekore as tk

from pathlib import Path
from dataclasses import dataclass
from typing import NamedTuple
import time

SPOTIFY_CONF_FILE = 'spoti_secret.cfg'

def get_new_token(client_id, client_secret):
    # # 1. Get and save token
    # # https://developer.spotify.com/

    # client_id = ''
    # client_secret = ''

    redirect_uri = 'https://example.com/callback'   # Or your redirect uri
    conf = (client_id, client_secret, redirect_uri)

    token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)
    tk.config_to_file(SPOTIFY_CONF_FILE, conf + (token.refresh_token,))
    

def load_token():
    conf = tk.config_from_file(SPOTIFY_CONF_FILE, return_refresh=True)
    token = tk.refresh_user_token(*conf[:2], conf[3])
    return token