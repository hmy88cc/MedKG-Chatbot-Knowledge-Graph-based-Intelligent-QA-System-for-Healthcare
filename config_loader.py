# coding: utf-8

import os
import yaml
from typing import Dict, Any, List


class Config:
    def __init__(self, config_path: str = "config.yaml"):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        keys = key_path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value
    
    @property
    def neo4j_config(self) -> Dict[str, Any]:
        return self._config.get('neo4j', {})
    
    @property
    def model_config(self) -> Dict[str, Any]:
        return self._config.get('model', {})
    
    @property
    def ner_config(self) -> Dict[str, Any]:
        return self._config.get('model', {}).get('ner', {})
    
    @property
    def classifier_config(self) -> Dict[str, Any]:
        return self._config.get('model', {}).get('classifier', {})
    
    @property
    def chatbot_config(self) -> Dict[str, Any]:
        return self._config.get('chatbot', {})
    
    @property
    def logging_config(self) -> Dict[str, Any]:
        return self._config.get('logging', {})
    
    @property
    def entity_types(self) -> Dict[str, str]:
        return self._config.get('entity_types', {})
    
    @property
    def question_labels(self) -> Dict[int, str]:
        return {int(k): v for k, v in self._config.get('question_labels', {}).items()}
