import os
from typing import Tuple, List

# microservice socket host und port storage location
to_load: List[Tuple[str, str]] = [
    ('STORAGE_LOCATION', 'db_data/'),
]

# the final configuration dict
config: dict = {}

# load all configuration values from the env
for key in to_load:
    if isinstance(key, tuple):
        if key[0] in os.environ:
            config[key[0]] = os.environ.get(key[0])
        else:
            config[key[0]] = key[1]
    elif key in os.environ:
        config[key] = os.environ.get(key)
