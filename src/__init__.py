import os
import sys
import logging.config
import threading
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
load_dotenv(dotenv_path='.env.local', override=True)

thread_local = threading.local()