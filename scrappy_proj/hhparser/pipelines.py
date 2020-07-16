# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class HhparserPipeline:
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.vacansy123


    def process_item(self, item, spider):
        if spider.name == 'superjobru':
            item['salary_min'], item['salary_max'], item['currency'] = self.process_salary_sj(item['salary'])
            del item['salary']

        if spider.name == 'hhru':
            item['salary_min'],item['salary_max'],item['currency'] = self.process_salary_hh(item['salary'])
            del item['salary']


        collection = self.mongo_base[spider.name]
        collection.insert_one(item)


        return item

    def __del__(self):
        self.client.close()


    def process_salary_hh(self, vacancy_salary):
        salary_min = None
        salary_max = None
        currency = None
        if vacancy_salary != None:
            vacancy_salary = vacancy_salary.replace(u'\xa0', u'')
            # print(vacancy_salary)
            salaries = vacancy_salary.split('-')
            if len(salaries) > 1:
                salary_min = int(salaries[0])
                salaries_1 = salaries[1].split(' ')
                if len(salaries_1) > 1:
                    salary_max = int(salaries_1[0])
                    currency = salaries_1[1]
                else:
                    salary_max = int(salaries_1[0])
            else:
                salaries_1 = vacancy_salary.split('от ')
                if len(salaries_1) > 1:
                    salaries_2 = salaries_1[1].split(' ')
                    salary_min = int(salaries_2[0])
                    if len(salaries_2) > 1:
                        currency = salaries_2[1]
                else:
                    salaries_2 = vacancy_salary.split('до ')
                    if len(salaries_2) > 1:
                        salaries_3 = salaries_2[1].split(' ')
                        salary_max = int(salaries_3[0])
                        if len(salaries_3) > 1:
                            currency = salaries_3[1]
                    else:
                        salary_min = int(vacancy_salary)
                        salary_max = int(vacancy_salary)

        return ([salary_min, salary_max, currency])


    def process_salary_sj(self, vacancy_salary):
        if vacancy_salary != None:
            salary_min = None
            salary_max = None
            currency = None
            vacancy_salary = vacancy_salary.replace(u'\xa0', u'')
            vacancy_salary = vacancy_salary.replace(u'руб.', u' руб')

            # print(vacancy_salary)
            if vacancy_salary != 'По договоренности' and vacancy_salary != 'По договорённости':
                vacancy_salary = vacancy_salary.replace(u'до', u'до ')
                vacancy_salary = vacancy_salary.replace(u'от', u'от ')
                salaries = vacancy_salary.split('—')
                if len(salaries) > 1:
                    salary_min = int(salaries[0])
                    salaries_1 = salaries[1].split(' ')
                    if len(salaries_1) > 1:
                        salary_max = int(salaries_1[0])
                        currency = salaries_1[1]
                    else:
                        salary_max = int(salaries_1[0])
                else:
                    salaries_1 = vacancy_salary.split('от ')
                    if len(salaries_1) > 1:
                        salaries_2 = salaries_1[1].split(' ')
                        salary_min = int(salaries_2[0])
                        if len(salaries_2) > 1:
                            currency = salaries_2[1]
                    else:
                        salaries_2 = vacancy_salary.split('до ')
                        if len(salaries_2) > 1:
                            salaries_3 = salaries_2[1].split(' ')
                            salary_max = int(salaries_3[0])
                            if len(salaries_3) > 1:
                                currency = salaries_3[1]
                        else:
                            print(vacancy_salary)
                            salaries_1 = vacancy_salary.split(' ')
                            salary_min = int(salaries_1[0])
                            salary_max = int(salaries_1[0])
                            if len(salaries_1) > 1:
                                currency = salaries_1[1]


        return ([salary_min, salary_max, currency])