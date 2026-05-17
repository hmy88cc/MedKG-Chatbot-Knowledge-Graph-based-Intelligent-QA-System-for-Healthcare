# coding: utf-8

from typing import Dict, List, Any
from py2neo import Graph
from logger_utils import LoggerManager

logger = LoggerManager.get_logger(__name__)

class AnswerSearcher:
    def __init__(self, config: Any = None):
        if config:
            neo4j_config = config.neo4j_config
            self.g = Graph(
                host=neo4j_config.get("host", "172.24.30.243"),
                http_port=neo4j_config.get("http_port", 7474),
                user=neo4j_config.get("user", "neo4j"),
                password=neo4j_config.get("password", "12345")
            )
            self.num_limit = config.chatbot_config.get("answer_limit", 20)
        else:
            self.g = Graph(
                host="172.24.30.243",
                http_port=7474,
                user="neo4j",
                password="12345"
            )
            self.num_limit = 20
        logger.info("AnswerSearcher 初始化成功")

    def search_main(self, sqls: List[Dict[str, Any]]) -> List[str]:
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                try:
                    ress = self.g.run(query).data()
                    answers += ress
                except Exception as e:
                    logger.error(f"执行查询失败: {query}, 错误: {e}")
                    continue
            final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        logger.info(f"搜索完成，生成 {len(final_answers)} 个答案")
        return final_answers

    def answer_prettify(self, question_type: str, answers: List[Dict]) -> List[str]:
        final_answer = []
        if not answers:
            return ''
        if question_type == 'disease_symptom':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}的症状包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'symptom_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = ['症状{0}可能染上的疾病有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_cause':
            desc = [i['m.cause'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}可能的成因有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_prevent':
            desc = [i['m.prevent'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}的预防措施包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_lasttime':
            desc = [i['m.cure_lasttime'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}治疗可能持续的周期为：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_cureway':
            desc = [';'.join(i['m.cure_way']) if isinstance(i['m.cure_way'], list) else i['m.cure_way'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}可以尝试如下治疗：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_cureprob':
            desc = [i['m.cured_prob'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}治愈的概率为（仅供参考）：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_easyget':
            desc = [i['m.easy_get'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}的易感人群包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_desc':
            desc = [i['m.desc'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}简介：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_acompany':
            desc1 = [i['n.name'] for i in answers]
            desc2 = [i['m.name'] for i in answers]
            subject = answers[0]['m.name']
            desc = [i for i in desc1 + desc2 if i != subject]
            final_answer = ['{0}的并发症包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_not_food':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}忌食的食物包括有：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_do_food':
            do_desc = [i['n.name'] for i in answers if i['r.name'] == '宜吃']
            recommand_desc = [i['n.name'] for i in answers if i['r.name'] == '推荐食谱']
            subject = answers[0]['m.name']
            final_answer = ['{0}宜食的食物包括有：{1}\n推荐食谱包括有：{2}'.format(subject, ';'.join(list(set(do_desc))[:self.num_limit]), ';'.join(list(set(recommand_desc))[:self.num_limit]))]

        elif question_type == 'food_not_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = ['患有{0}的人最好不要吃{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)]

        elif question_type == 'food_do_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = ['患有{0}的人建议多试试{1}'.format('；'.join(list(set(desc))[:self.num_limit]), subject)]

        elif question_type == 'disease_drug':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}通常的使用的药品包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'drug_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = ['{0}主治的疾病有{1},可以试试'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_check':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}通常可以通过以下方式检查出来：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'check_disease':
            desc = [i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = ['通常可以通过{0}检查出来的疾病有{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'symptom_curway':
            desc = [';'.join(i['m.cure_way']) if isinstance(i['m.cure_way'], list) else i['m.cure_way'] for i in answers]
            subject = answers[0]['n.name']
            final_answer = ['具有{0}症状的疾病治疗方法包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'drug_side_effect':
            desc = [i['m.desc'] for i in answers if 'm.desc' in i]
            subject = answers[0]['n.name']
            final_answer = ['{0}相关说明：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'drug_usage':
            desc = [';'.join(i['m.cure_way']) if isinstance(i['m.cure_way'], list) else str(i['m.cure_way']) for i in answers if 'm.cure_way' in i]
            subject = answers[0]['n.name']
            final_answer = ['{0}的使用方式：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'department_recommend':
            desc = [i['m.cure_department'] for i in answers if 'm.cure_department' in i]
            subject = answers[0]['n.name']
            final_answer = ['症状{0}建议就诊科室：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_body_part':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}可能影响的部位包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_surgery':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}可能需要的手术方式包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        elif question_type == 'disease_insurance':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = ['{0}的医保覆盖类型包括：{1}'.format(subject, '；'.join(list(set(desc))[:self.num_limit]))]

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
