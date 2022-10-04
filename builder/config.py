from pathlib import Path
import yaml
import logging
import json

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_DATA = yaml.safe_load(open(f'{BASE_DIR}/config.yaml','r'))

def get_value(key):
    return SITE_DATA[key]
    
class Config:
    CONTENT_DIR = f"{BASE_DIR}/content"
    LAYOUT_DIR = f"{BASE_DIR}/layout"
    STATIC_SRC_PATH = f"{BASE_DIR}/static"
    DIST_SRC_PATH = f"{BASE_DIR}/dist/static"
    SITE_NAME = get_value('site_name')
    SITE_DESCRIPTION = get_value('site_description')
    SITE_KEYWORDS = get_value('site_keywords')
    SITE_AUTHOR = get_value('site_author')