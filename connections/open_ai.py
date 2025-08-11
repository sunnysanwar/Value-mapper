import openai
from config.index import OPENAI_API_KEY, OPENAI_ORGANIZATION

def auth_openai():
    if OPENAI_ORGANIZATION:
        openai.organization = OPENAI_ORGANIZATION
    openai.api_key = OPENAI_API_KEY
    return openai