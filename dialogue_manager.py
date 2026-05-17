# coding: utf-8

from typing import Dict, List, Any, Optional
from collections import deque
import time
from logger_utils import LoggerManager

logger = LoggerManager.get_logger(__name__)

class DialogueContext:
    def __init__(self, max_turns: int = 5):
        self.max_turns = max_turns
        self.history: deque = deque(maxlen=max_turns)
        self.last_entities: Dict[str, List[str]] = {}
        self.last_question_type: Optional[str] = None
        self.last_answer: Optional[str] = None
        self.session_start_time: float = time.time()
        
    def add_turn(self, question: str, answer: str, entities: Dict[str, List[str]], question_type: str):
        self.history.append({
            'question': question,
            'answer': answer,
            'entities': entities,
            'question_type': question_type,
            'timestamp': time.time()
        })
        self.last_entities = entities
        self.last_question_type = question_type
        self.last_answer = answer
        
    def get_last_entities(self) -> Dict[str, List[str]]:
        return self.last_entities
        
    def get_last_question_type(self) -> Optional[str]:
        return self.last_question_type
        
    def is_timeout(self, timeout: int = 300) -> bool:
        return (time.time() - self.session_start_time) > timeout
        
    def clear(self):
        self.history.clear()
        self.last_entities = {}
        self.last_question_type = None
        self.last_answer = None
        self.session_start_time = time.time()
        
    def get_history(self) -> List[Dict]:
        return list(self.history)


class DialogueManager:
    def __init__(self, max_context_turns: int = 5, context_timeout: int = 300):
        self.max_context_turns = max_context_turns
        self.context_timeout = context_timeout
        self.contexts: Dict[str, DialogueContext] = {}
        logger.info(f"DialogueManager 初始化，最大上下文轮数: {max_context_turns}, 超时时间: {context_timeout}秒")
    
    def get_context(self, session_id: str = "default") -> DialogueContext:
        if session_id not in self.contexts:
            self.contexts[session_id] = DialogueContext(max_turns=self.max_context_turns)
        context = self.contexts[session_id]
        if context.is_timeout(self.context_timeout):
            logger.info(f"会话 {session_id} 超时，重置上下文")
            context.clear()
        return context
    
    def update_context(self, session_id: str, question: str, answer: str, 
                      entities: Dict[str, List[str]], question_type: str):
        context = self.get_context(session_id)
        context.add_turn(question, answer, entities, question_type)
        logger.debug(f"更新会话 {session_id} 上下文，当前轮数: {len(context.history)}")
    
    def resolve_ellipsis(self, question: str, session_id: str = "default") -> str:
        context = self.get_context(session_id)
        if not context.last_entities:
            return question
            
        ellipsis_keywords = ['呢', '那', '这个', '那个', '它', '他', '她', '有哪些', '是什么', '怎么办']
        has_ellipsis = any(keyword in question for keyword in ellipsis_keywords)
        
        if has_ellipsis and context.last_entities:
            for entity_type, entities in context.last_entities.items():
                if entities:
                    for entity in entities:
                        question = question.replace('呢', f'的{entity_type}呢').replace('那个', entity).replace('这个', entity)
                        break
                    break
        return question
    
    def merge_entities(self, question_entities: Dict[str, List[str]], 
                      session_id: str = "default") -> Dict[str, List[str]]:
        context = self.get_context(session_id)
        merged_entities = dict(context.last_entities)
        
        for entity_type, entities in question_entities.items():
            if entity_type not in merged_entities:
                merged_entities[entity_type] = entities
            else:
                merged_entities[entity_type] = list(set(merged_entities[entity_type] + entities))
        
        return merged_entities
    
    def clear_session(self, session_id: str = "default"):
        if session_id in self.contexts:
            del self.contexts[session_id]
            logger.info(f"清除会话 {session_id} 上下文")
    
    def get_context_summary(self, session_id: str = "default") -> str:
        context = self.get_context(session_id)
        if not context.history:
            return "无对话历史"
        
        summary_parts = []
        for i, turn in enumerate(context.history[-3:], 1):
            summary_parts.append(f"Q{i}: {turn['question'][:20]}...")
        return " | ".join(summary_parts)
