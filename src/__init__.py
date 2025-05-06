import os
import sys
import logging.config
import threading
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
load_dotenv(dotenv_path='.env.local', override=True)

thread_local = threading.local()

# --- Logging config ---
ELASTICSEARCH_HOST = 'homestock-elasticsearch'
ELASTICSEARCH_PORT = 9200
ELASTICSEARCH_USE_SSL = False 
ELASTICSEARCH_VERIFY_SSL = True 

LOG_BUFFER_PATH = 'logs'
LOG_BUFFER_DB = os.path.join(LOG_BUFFER_PATH, 'logstash_buffer.db')

os.makedirs(LOG_BUFFER_PATH, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout
        },
        'elasticsearch_async': {
            'level': 'INFO',
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            'host': ELASTICSEARCH_HOST,
            'port': ELASTICSEARCH_PORT,
            'database_path': LOG_BUFFER_DB,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'elasticsearch_async'],
            'level': 'DEBUG'
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__) # o logging.getLogger('mi_modulo_especifico')

logger.debug("Este es un mensaje de depuración (solo consola).")
logger.info("Iniciando la aplicación de ejemplo.")
logger.info(f"Enviando logs a Elasticsearch en {ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}")
