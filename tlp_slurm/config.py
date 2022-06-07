# !/usr/bin/python
# -*- coding:utf-8 -*-
from pathlib import Path
import platform

is_windows = (platform.system() == 'Windows')
DATA_DIR = 'data'
SCRIPT_DIR = 'script'
ARGS_FILE = Path(__file__).resolve().parent / 'args.json'


# BASE_PATH = Path(__file__).resolve().parent.parent.parent
