# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from instagram.items import InstagramItem
import re
import json
from urllib.parse import urlencode
from copy import deepcopy


class InstagramSpider(scrapy.Spider):
    #атрибуты класса
    name = 'insta'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'mashine_learning'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER:10:1595269695:AfJQADxArCZVKxfEZJd5mayPcBz3eOhpPgRppAonBxnlZEAnePzROnOLSXeUXVhE7muBOR2B2EakcZzT5/Oj3JbgHCS36SJmUbJpbZqAxUkJ5aMZSZjzt3fP8B1nFo3NCYOkeQPte1q0bKUA'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_user = ['diana__vorobeva', 'lubovlvovna41' ]     #Парсим маму и бабушку
    #parse_user = ['diana__vorobeva']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followers_hash = 'c76146de99bb02f6415203be841dd25a' #hash для получения данных по подписчиках с главной страницы
    following_hash = 'd04b0a864b4b54837c0d870b0e77e076' #hash для получения данных по подпискахх с главной страницы
    numb_diana = 0
    numb_julia = 0
    def parse(self, response:HtmlResponse):             #Первый запрос на стартовую страницу
        csrf_token = self.fetch_csrf_token(response.text)   #csrf token забираем из html
        yield scrapy.FormRequest(                   #заполняем форму для авторизации
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username':self.insta_login, 'enc_password':self.insta_pwd},
            headers={'X-CSRFToken':csrf_token}
        )

    def user_parse(self, response:HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:                 #Проверяем ответ после авторизации
            for one_user in self.parse_user:
                yield response.follow(                  #Переходим на желаемую страницу пользователя в цикле
                    f'/{one_user}',
                    callback= self.user_data_parse,
                    cb_kwargs={'username': deepcopy(one_user)}
            )




    def user_data_parse(self, response:HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)       #Получаем id пользователя
        variables={'id':user_id,                                    #Формируем словарь для передачи даных в запрос
                   'first':14
                   }                                      #14 подписчиков
        url_followers = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'    #Формируем ссылку для получения данных о подписчиках
        yield response.follow(
            url_followers,
            callback=self.user_followers_parse,
            cb_kwargs={'username':deepcopy(username),           #username ч/з deepcopy во избежание гонок
                       'user_id':deepcopy(user_id),             #user_id ч/з deepcopy во избежание гонок
                       'variables':deepcopy(variables)}         #variables ч/з deepcopy во избежание гонок
        )

        url_following = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(variables)}'

        yield response.follow(
            url_following,
            callback=self.user_following_parse,
            cb_kwargs={'username': deepcopy(username),  #username ч/з deepcopy во избежание гонок
                       'user_id': deepcopy(user_id),    #user_id ч/з deepcopy во избежание гонок
                       'variables': deepcopy(variables)}  # variables ч/з deepcopy во избежание гонок
        )



    def user_followers_parse(self, response:HtmlResponse,username,user_id,variables):   #Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        followers = j_data.get('data').get('user').get('edge_followed_by').get('edges')  # Сами посты
        for follower in followers:  # Перебираем подписчиков, собираем данные
            item = InstagramItem(
                follower=follower['node']['id'],
                # follower='gg',
                full_name_follower=follower['node']['full_name'],
                user_id=user_id,
                photo=follower['node']['profile_pic_url'],
                isfollower=True
            )
            yield item  # В пайплайн

        page_info = j_data.get('data').get('user').get('edge_followed_by').get('page_info')
        if page_info.get('has_next_page'):                                          #Если есть следующая страница
            variables['after'] = page_info['end_cursor']                            #Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.followers_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_followers_parse,
                cb_kwargs={'username': deepcopy(username),
                           'user_id': deepcopy(user_id),
                           'variables': deepcopy(variables)}
            )


    def user_following_parse(self, response: HtmlResponse, username, user_id,
                             variables):  # Принимаем ответ. Не забываем про параметры от cb_kwargs
        j_data = json.loads(response.text)
        followings = j_data.get('data').get('user').get('edge_follow').get('edges')  # Сами подписки
        for following in followings:  # Перебираем подписки, собираем данные
            item = InstagramItem(
                follower=following['node']['id'],
                # follower='gg',
                full_name_follower=following['node']['full_name'],
                user_id=user_id,
                photo=following['node']['profile_pic_url'],
                isfollower=False
            )
            yield item

        page_info = j_data.get('data').get('user').get('edge_follow').get('page_info')
        if page_info.get('has_next_page'):  # Если есть следующая страница
            variables['after'] = page_info['end_cursor']  # Новый параметр для перехода на след. страницу
            url_posts = f'{self.graphql_url}query_hash={self.following_hash}&{urlencode(variables)}'
            yield response.follow(
                url_posts,
                callback=self.user_following_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )






        #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')