# coding: utf-8

from typing import Dict, List, Any
from logger_utils import LoggerManager

logger = LoggerManager.get_logger(__name__)

class QuestionPaser:

    def build_entitydict(self, args: Dict[str, List[str]]) -> Dict[str, List[str]]:
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)
        return entity_dict

    def parser_main(self, res_classify: Dict[str, Any]) -> List[Dict[str, Any]]:
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            
            if question_type == 'disease_symptom':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'symptom_disease' or question_type == 'symptom_curway':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))
            elif question_type == 'disease_drug':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'drug_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            elif question_type == 'disease_check':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_prevent':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_lasttime':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_cureway':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_desc':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_cause':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_acompany':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'drug_side_effect':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            elif question_type == 'drug_usage':
                sql = self.sql_transfer(question_type, entity_dict.get('drug'))
            elif question_type == 'department_recommend':
                sql = self.sql_transfer(question_type, entity_dict.get('symptom'))
            elif question_type == 'disease_cureprob':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_easyget':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_not_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_do_food':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'food_not_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))
            elif question_type == 'food_do_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('food'))
            elif question_type == 'check_disease':
                sql = self.sql_transfer(question_type, entity_dict.get('check'))
            elif question_type == 'disease_body_part':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_surgery':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            elif question_type == 'disease_insurance':
                sql = self.sql_transfer(question_type, entity_dict.get('disease'))
            else:
                logger.warning(f"未知的问句类型: {question_type}")

            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)

        logger.info(f"解析生成 {len(sqls)} 条SQL查询")
        return sqls

    def sql_transfer(self, question_type: str, entities: List[str]) -> List[str]:
        if not entities:
            return []

        sql = []
        
        if question_type == 'disease_cause':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cause".format(i) for i in entities]

        elif question_type == 'disease_prevent':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.prevent".format(i) for i in entities]

        elif question_type == 'disease_lasttime':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_lasttime".format(i) for i in entities]

        elif question_type == 'disease_cureprob':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cured_prob".format(i) for i in entities]

        elif question_type == 'disease_cureway':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]

        elif question_type == 'disease_easyget':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.easy_get".format(i) for i in entities]

        elif question_type == 'disease_desc':
            sql = ["MATCH (m:Disease) where m.name = '{0}' return m.name, m.desc".format(i) for i in entities]

        elif question_type == 'disease_symptom':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'symptom_disease':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_acompany':
            sql1 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2
            
        elif question_type == 'disease_not_food':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_do_food':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        elif question_type == 'food_not_disease':
            sql = ["MATCH (m:Disease)-[r:no_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'food_do_disease':
            sql1 = ["MATCH (m:Disease)-[r:do_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_eat]->(n:Food) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        elif question_type == 'disease_drug':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2

        elif question_type == 'drug_disease':
            sql1 = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql2 = ["MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            sql = sql1 + sql2
            
        elif question_type == 'disease_check':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'check_disease':
            sql = ["MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]
            
        elif question_type == 'symptom_curway':
            sql1 = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]
            
        elif question_type == 'drug_side_effect':
            sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, m.desc".format(i) for i in entities]
            
        elif question_type == 'drug_usage':
            sql = ["MATCH (m:Disease)-[r:common_drug]->(n:Drug) where n.name = '{0}' return m.name, m.cure_way".format(i) for i in entities]
            
        elif question_type == 'department_recommend':
            sql = ["MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{0}' return m.cure_department".format(i) for i in entities]

        elif question_type == 'disease_body_part':
            sql = ["MATCH (m:Disease)-[r:affects_body_part]->(n:BodyPart) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_surgery':
            sql = ["MATCH (m:Disease)-[r:requires_surgery]->(n:Surgery) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        elif question_type == 'disease_insurance':
            sql = ["MATCH (m:Disease)-[r:covered_by_insurance]->(n:Insurance) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql



if __name__ == '__main__':
    from question_classifier import *

    handler = QuestionPaser()
    QChandler = QuestionClassifier()
    while 1:
        question = input(' input an question:')
        data = QChandler.classify(question)
        print(data)
        sqls = handler.parser_main(data)
        print(sqls)
