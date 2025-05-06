import logging
import logging.config
import sys
import time
import os # Para crear directorio de buffer

# --- Configuración de Conexión a Elasticsearch ---
# ¡¡¡IMPORTANTE!!! REEMPLAZA ESTOS VALORES CON LOS TUYOS
ELASTICSEARCH_HOST = 'localhost'   # Host o IP de tu servidor Elasticsearch
ELASTICSEARCH_PORT = 9200          # Puerto de tu servidor Elasticsearch (suele ser 9200)
# ELASTICSEARCH_USERNAME = None      # Descomenta y pon tu usuario si ES tiene seguridad
# ELASTICSEARCH_PASSWORD = None      # Descomenta y pon tu contraseña si ES tiene seguridad
ELASTICSEARCH_USE_SSL = False      # Cambia a True si usas HTTPS para conectar a ES
ELASTICSEARCH_VERIFY_SSL = True    # Cambia a False si usas cert autofirmado y quieres saltar verificación
# --------------------------------------------------

# Ruta para el archivo de buffer (guarda logs si ES no está disponible)
LOG_BUFFER_PATH = 'logs'
LOG_BUFFER_DB = os.path.join(LOG_BUFFER_PATH, 'logstash_buffer.db')

# Crear directorio para el buffer si no existe
os.makedirs(LOG_BUFFER_PATH, exist_ok=True)


# --- Diccionario de Configuración de Logging ---
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False, # No deshabilitar loggers de librerías
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        # Nota: AsynchronousLogstashHandler suele enviar un JSON bien estructurado
        # por defecto, un formatter específico aquí puede no ser necesario
        # a menos que quieras personalizar mucho el payload.
    },
    'handlers': {
        'console': {
            'level': 'DEBUG', # Nivel mínimo para mostrar en consola
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout, # Usar salida estándar
        },
        # --- Handler para python-logstash-async ---
        'elasticsearch_async': {
            'level': 'INFO', # Nivel mínimo para ENVIAR a Elasticsearch
            'class': 'logstash_async.handler.AsynchronousLogstashHandler',
            # --- Parámetros de conexión ---
            'host': ELASTICSEARCH_HOST,
            'port': ELASTICSEARCH_PORT,
            'database_path': LOG_BUFFER_DB, # Ruta al archivo de buffer
            # --- Seguridad (Descomentar y ajustar si es necesario) ---
            # 'username': ELASTICSEARCH_USERNAME,
            # 'password': ELASTICSEARCH_PASSWORD,
            # 'ssl_enable': ELASTICSEARCH_USE_SSL,
            # 'ssl_verify': ELASTICSEARCH_VERIFY_SSL,
        }
        # --------------------------------------
    },
    'loggers': {
        '': { # Logger Raíz - Configuración por defecto para toda la app
            'handlers': ['console', 'elasticsearch_async'], # Aplica ambos handlers
            'level': 'DEBUG', # Nivel mínimo que el logger procesará
                              # El nivel del HANDLER decide qué se envía realmente
                              # (DEBUG->Consola, INFO->Elasticsearch en este caso)
        },
        'mi_modulo_especifico': { # Ejemplo de logger específico
            'handlers': ['console', 'elasticsearch_async'],
            'level': 'DEBUG',
            'propagate': False, # Evita que los logs de este logger lleguen también al raíz
        },
        'urllib3': { # Silenciar librería ruidosa (ejemplo)
             'handlers': ['console'], # Solo a consola para ver si hay errores
             'level': 'WARNING',
             'propagate': False,
        }
    }
}

# --- Función principal de la aplicación ---
def main():
    # Obtener un logger para este módulo (o usar uno específico como 'mi_modulo_especifico')
    logger = logging.getLogger(__name__) # o logging.getLogger('mi_modulo_especifico')

    logger.debug("Este es un mensaje de depuración (solo consola).")
    logger.info("Iniciando la aplicación de ejemplo.")
    logger.info(f"Enviando logs a Elasticsearch en {ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}")

    for i in range(3):
        logger.info(f"Procesando item {i+1}")
        time.sleep(0.5)

    logger.warning("Se detectó una condición inesperada pero manejable.")

    try:
        # Simular un error
        valor = 10 / 0
    except ZeroDivisionError:
        # logger.exception es ideal para errores, incluye el traceback
        logger.exception("¡Se ha producido un error de división por cero!")

    logger.error("Este es un mensaje de error genérico después de la excepción.")
    logger.info("Aplicación finalizando.")

# --- Punto de Entrada Principal ---
if __name__ == "__main__":
    print("Configurando el sistema de logging...")
    # --- Aplicar la configuración de logging UNA SOLA VEZ ---
    logging.config.dictConfig(LOGGING_CONFIG)
    # -------------------------------------------------------
    print("Logging configurado.")

    # Ejecutar la lógica principal
    main()

    # --- Importante para handlers asíncronos ---
    # Dar tiempo a que los logs en buffer se envíen antes de que el script termine.
    # En aplicaciones reales/servicios, esto se maneja mejor con
    # logging.shutdown() durante el apagado ordenado (e.g., usando atexit).
    print("Esperando para asegurar el envío de logs asíncronos...")
    time.sleep(5) # Ajusta este tiempo si es necesario
    print("Script terminado.")

    # Alternativa más robusta para el cierre:
    # import atexit
    # atexit.register(logging.shutdown)