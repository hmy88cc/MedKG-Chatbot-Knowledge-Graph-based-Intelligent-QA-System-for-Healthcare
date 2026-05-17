# coding: utf-8

from typing import Optional
from question_parser import QuestionPaser
from answer_search import AnswerSearcher
from question_analysis import QuestionAnalysis
from dialogue_manager import DialogueManager
from config_loader import Config
from logger_utils import LoggerManager

logger = LoggerManager.get_logger(__name__)

class ChatBotGraph:
    def __init__(self, config_path: Optional[str] = None):
        try:
            if config_path:
                self.config = Config(config_path)
            else:
                self.config = Config()
            
            self.classifier = QuestionAnalysis(self.config)
            self.parser = QuestionPaser()
            self.searcher = AnswerSearcher(self.config)
            
            dialogue_config = self.config.chatbot_config.get('dialogue', {})
            self.dialogue_manager = DialogueManager(
                max_context_turns=dialogue_config.get('max_context_turns', 5),
                context_timeout=dialogue_config.get('context_timeout', 300)
            )
            
            self.default_answer = self.config.chatbot_config.get('default_answer', '您的问题我还不能理解，请换个问法')
            logger.info("ChatBotGraph 初始化成功")
            
        except Exception as e:
            logger.error(f"ChatBotGraph 初始化失败: {e}")
            raise

    def chat_main(self, sent: str, session_id: str = "default") -> str:
        try:
            logger.info(f"收到用户输入 (会话: {session_id}): {sent}")
            
            resolved_question = self.dialogue_manager.resolve_ellipsis(sent, session_id)
            
            res_classify = self.classifier.analysis(resolved_question)
            logger.debug(f"分类结果: {res_classify}")
            
            if not res_classify:
                return self.default_answer
                
            res_sql = self.parser.parser_main(res_classify)
            final_answers = self.searcher.search_main(res_sql)
            
            if not final_answers:
                answer = self.default_answer
            else:
                answer = '\n'.join(final_answers)
            
            self.dialogue_manager.update_context(
                session_id, 
                sent, 
                answer, 
                res_classify.get('args', {}), 
                res_classify.get('question_types', [''])[0]
            )
            
            logger.info(f"生成回答: {answer[:50]}...")
            return answer
            
        except Exception as e:
            logger.error(f"处理问题失败: {sent}, 错误: {e}")
            return f"抱歉，处理您的问题时出现了错误：{str(e)}"

    def clear_context(self, session_id: str = "default"):
        self.dialogue_manager.clear_session(session_id)
        logger.info(f"清除会话 {session_id} 的上下文")

    def get_context_summary(self, session_id: str = "default") -> str:
        return self.dialogue_manager.get_context_summary(session_id)


if __name__ == '__main__':
    import sys
    
    handler = ChatBotGraph()
    
    print('=' * 60)
    print('您好，我是医疗聊天机器人李雯φ(゜▽゜*)♪')
    print('请问您想了解什么，希望我的回答可以帮到您！')
    print('输入 "quit" 或 "exit" 退出，输入 "clear" 清除对话上下文')
    print('=' * 60)
    
    session_id = "default"
    question = ''
    
    while question not in ["quit", "exit", "", " "]:
        try:
            question = input('用户: ').strip()
            
            if question in ["quit", "exit", "", " "]:
                break
                
            if question.lower() == 'clear':
                handler.clear_context(session_id)
                print('李雯: 对话上下文已清除')
                continue
                
            if question.lower() == 'summary':
                summary = handler.get_context_summary(session_id)
                print(f'李雯: 当前对话摘要: {summary}')
                continue
                
            answer = handler.chat_main(question, session_id)
            print('李雯:', answer)
            
        except KeyboardInterrupt:
            print('\n再见！')
            sys.exit(0)
        except Exception as e:
            logger.error(f"主循环异常: {e}")
            print('李雯: 抱歉，系统出现异常，请重试')
    
    print('再见！')
