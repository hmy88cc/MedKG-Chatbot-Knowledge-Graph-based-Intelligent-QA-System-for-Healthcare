# coding: utf-8

import os
import logging
from logging.handlers import RotatingFileHandler
from config_loader import Config


class LoggerManager:
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str, config: Config = None) -> logging.Logger:
        if name in cls._loggers:
            return cls._loggers[name]
        
        if config is None:
            config = Config()
        
        log_config = config.logging_config
        log_level = getattr(logging, log_config.get('level', 'INFO').upper())
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_file = log_config.get('file', 'logs/chatbot.log')
        max_bytes = log_config.get('max_bytes', 10485760)
        backup_count = log_config.get('backup_count', 5)
        
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        
        if not logger.handlers:
            formatter = logging.Formatter(log_format)
            
            file_handler = RotatingFileHandler(
                log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        
        cls._loggers[name] = logger
        return logger
