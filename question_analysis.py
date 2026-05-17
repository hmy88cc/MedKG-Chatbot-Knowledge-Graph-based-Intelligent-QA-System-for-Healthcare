# coding: utf-8

import os
from typing import Dict, List, Tuple, Any, Optional
import tensorflow as tf
from classifyApp import classifyApplication
from nerApp import nerAppication
from config_loader import Config
from logger_utils import LoggerManager

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

logger = LoggerManager.get_logger(__name__)

class QuestionAnalysis:
    def __init__(self, config: Optional[Config] = None, device: str = '/cpu:0'):
        self.config = config
        self.device = device
        
        if config:
            model_config = config.model_config
            gpu_memory_fraction = model_config.get('gpu_memory_fraction', 0.3)
            allow_soft_placement = model_config.get('allow_soft_placement', True)
            log_device_placement = model_config.get('log_device_placement', False)
        else:
            gpu_memory_fraction = 0.3
            allow_soft_placement = True
            log_device_placement = False
            
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
        session_conf = tf.ConfigProto(
            gpu_options=gpu_options,
            allow_soft_placement=allow_soft_placement,
            log_device_placement=log_device_placement
        )
        
        self.g1 = tf.Graph()
        self.g2 = tf.Graph()
        self.sess_ner = tf.Session(graph=self.g1, config=session_conf)
        self.sess_classify = tf.Session(graph=self.g2, config=session_conf)
        
        try:
            self.classifyApp = classifyApplication(self.sess_classify, device)
            self.nerApp = nerAppication(self.sess_ner, device)
            logger.info("模型加载成功")
        except Exception as e:
            logger.error(f"模型加载失败: {e}")
            raise
        
        self.id2state = {
            0: 'O',
            1: 'B-dis', 2: 'I-dis', 3: 'E-dis', 10: 'S-dis',
            4: 'B-sym', 5: 'I-sym', 6: 'E-sym', 11: 'S-sym',
            7: 'B-dru', 8: 'I-dru', 9: 'E-dru', 12: 'S-dru',
            13: 'B-dep', 14: 'I-dep', 15: 'E-dep', 16: 'S-dep',
            17: 'B-chk', 18: 'I-chk', 19: 'E-chk', 20: 'S-chk',
            21: 'B-fod', 22: 'I-fod', 23: 'E-fod', 24: 'S-fod',
            25: 'B-bdy', 26: 'I-bdy', 27: 'E-bdy', 28: 'S-bdy',
            29: 'B-sur', 30: 'S-sur'
        }
        
        self.state2entityType = {
            'dis': 'disease', 'sym': 'symptom', 'dru': 'drug',
            'dep': 'department', 'chk': 'check', 'fod': 'food', 
            'bdy': 'body_part', 'sur': 'surgery', 'ins': 'insurance', 'prd': 'producer'
        }
        
        self.id2label = {
            0: "disease_symptom", 1: "symptom_curway", 2: "symptom_disease",
            3: "disease_drug", 4: "drug_disease", 5: "disease_check",
            6: "disease_prevent", 7: "disease_lasttime", 8: "disease_cureway",
            9: "disease_cause", 10: "disease_acompany", 11: "disease_desc",
            12: "drug_side_effect", 13: "drug_usage", 14: "department_recommend",
            15: "disease_body_part", 16: "disease_surgery", 17: "disease_insurance"
        }
        
        logger.info("QuestionAnalysis 初始化完成")

    def extract_entities(self, data_line: List[List[str]], label_line: List[List[int]], 
                        efficient_sequence_length: List[int]) -> Tuple[Dict[str, List[str]], str]:
        args = {}
        middle_question = []
        
        for idx in range(len(data_line)):
            _entity = ''
            for each in range(efficient_sequence_length[idx]):
                middle_question.append(data_line[idx][each])
                _entityType = self.id2state[int(label_line[idx][each])]
                
                if _entityType[0] in ['B', 'I']:
                    _entity += data_line[idx][each]
                elif _entityType[0] in ['E', 'S']:
                    _entity += data_line[idx][each]
                    _entityType_short = _entityType[-3:]
                    middle_question.append(self.state2entityType.get(_entityType_short, 'unknown'))
                    
                    if _entity not in args:
                        args.setdefault(_entity, [self.state2entityType.get(_entityType_short, 'unknown')])
                    else:
                        args[_entity].append(self.state2entityType.get(_entityType_short, 'unknown'))
                    _entity = ''
                else:
                    _entity = ''
        
        question_text = ''.join(middle_question)
        logger.debug(f"提取实体: {args}")
        return args, question_text

    def analysis(self, text: str) -> Dict[str, Any]:
        try:
            if not text or not text.strip():
                logger.warning("输入文本为空")
                return {}
                
            text = text.strip()
            logger.info(f"分析问题: {text}")
            
            data_line, label_line, efficient_sequence_length = self.nerApp.questionNer(self.sess_ner, text)
            
            args, question_text = self.extract_entities(data_line, label_line, efficient_sequence_length)
            
            classify_idx = self.classifyApp.questionClassify(self.sess_classify, question_text)
            question_type = self.id2label.get(classify_idx[0], "unknown")
            
            result = {
                'args': args,
                'question_types': [question_type]
            }
            
            logger.info(f"分析结果: {result}")
            return result
            
        except Exception as e:
            logger.error(f"问题分析失败: {text}, 错误: {e}")
            return {}


if __name__ == "__main__":
    ques = QuestionAnalysis()
    text = "我发烧流鼻涕怎么治疗"
    while(text != "" and text != " "):
        text = input("请输入一句话：")
        if text == "quit" or text == "" or text == " ":
            break
        res = ques.analysis(text)
        print(res)
