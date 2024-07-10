import json

with open("config.json", "r") as f:
    _config = json.load(f)


def OPENAI_API_KEY():
    return _config["openai_api_key"]


def PASSWORD_TTL_SECONDS():
    return _config["password_ttl_seconds"]


def PASSWORD_HASH():
    return _config["password_hash"]
