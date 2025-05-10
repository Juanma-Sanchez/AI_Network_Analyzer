import os

try:
    from local_settings import *
except:
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
