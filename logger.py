import logging
import os
from datetime import datetime

def setup_logger():
    # Maak logs directory als deze nog niet bestaat
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Genereer log bestandsnaam met timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/app_{timestamp}.log'
    
    # Configureer logger
    logger = logging.getLogger('ATK_WPBR')
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_format)
    
    # Voeg handlers toe aan logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Maak een globale logger instantie
logger = setup_logger() 