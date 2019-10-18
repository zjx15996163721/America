#!/usr/bin/env python3
import requests
from lxml import etree
import re
from get_cookie import Cookie
import pika
import yaml
import json
from category_orm import Category, SecondCategory, get_sqlalchemy_session
setting = yaml.load(open('config.yaml'))
db_session = get_sqlalchemy_session()


class Realtor:

    def __init__(self, cookie):
        self.start_url = 'https://www.realtor.com'
        self.headers = {
            'cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }

    def start(self):
        """
        入口
        :return:
        """
        r = requests.get(url=self.start_url, headers=self.headers)
        html = etree.HTML(r.text)
        category = html.xpath('//ul[@class="jsx-3652141321 list-unstyled link-secondary"]')[3]
        self.first_category(category)

    def first_category(self, category):
        """
        一级分类
        :param category: 分类对象
        :return:
        """
        category_list = category.xpath('./li')
        for i in category_list:
            category_url = i.xpath('./a/@href')[0]
            print(category_url)
            category_name = re.search('.*?realestateandhomes-search/(.*)', category_url, re.S | re.M).group(1)

            # 存mysql
            category = Category()
            category.category_name = category_name
            if db_session.query(Category).filter_by(category_name=category.category_name).first() is None:
                print(category_name)
                db_session.add(category)
                db_session.commit()
            else:
                print('已经存在')

            self.second_category(category_url, category_name)

    def second_category(self, category_url, category_name):
        """
        二级分类
        :param category_url: 一级分类的url
        :return:
        """
        second_category_url = category_url + '/counties'
        r = requests.get(url=second_category_url, headers=self.headers)
        html = etree.HTML(r.text)
        second_category_list = html.xpath('//li[@class="jsx-2588082720 list-column-item"]')
        for second_category in second_category_list:
            second_category_url_half = second_category.xpath('./a/@href')[0]
            second_category_url = 'https://www.realtor.com' + re.search('(/realestateandhomes-search/.*?)/explore', second_category_url_half, re.S | re.M).group(1)
            print(second_category_url)
            second_category_name = second_category.xpath('./a/span/text()')[0]

            # 存mysql
            second_category = SecondCategory()
            second_category.category_name = category_name
            second_category.second_category_name = second_category_name
            if db_session.query(SecondCategory).filter_by(category_name=second_category.category_name, second_category_name=second_category.second_category_name).first() is None:
                print(second_category_name)
                db_session.add(second_category)
                db_session.commit()
            else:
                print('已经存在')

            self.sale_house(second_category_url)
            self.sold_house(second_category_url)
            self.rent_house(second_category_url)

    def sale_house(self, second_category_url):
        """
        挂牌销售
        :param second_category_url:
        :return:
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbit']['host'],
                                                                       port=setting['rabbit']['port'],
                                                                       heartbeat=0))
        channel = connection.channel()
        total_page = self.get_max_page(second_category_url)
        for page in range(1, total_page + 1):
            page_url = second_category_url + '/pg-' + str(page)
            print(page_url)
            r = requests.get(url=page_url, headers=self.headers)
            html = etree.HTML(r.text)
            house_list = html.xpath("//li[@class='component_property-card js-component_property-card js-quick-view']")
            for house in house_list:
                house_id = 'M' + house.xpath("./@data-propertyid")[0]
                detail_url = 'http://www.realtor.com/property-overview/' + house_id
                data = {
                    'house_id': house_id,
                    'url': detail_url
                }
                channel.queue_declare(queue='list_price')
                channel.basic_publish(exchange='',
                                      routing_key='list_price',
                                      body=json.dumps(data))
                print('放队列 {}'.format(data))

    def sold_house(self, second_category_url):
        """
        已售出
        :param second_category_url:
        :return:
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbit']['host'],
                                                                       port=setting['rabbit']['port'],
                                                                       heartbeat=0))
        channel = connection.channel()
        total_page = self.get_max_page(second_category_url)
        sold_url = second_category_url.replace('realestateandhomes-search', 'soldhomeprices')
        for page in range(1, total_page + 1):
            page_url = sold_url + '/pg-' + str(page)
            print(page_url)
            r = requests.get(url=page_url, headers=self.headers)
            html = etree.HTML(r.text)
            house_list = html.xpath("//li[@class='component_property-card js-component_property-card js-quick-view']")
            for house in house_list:
                house_id = 'M' + house.xpath("./@data-propertyid")[0]
                detail_url = 'http://www.realtor.com/property-overview/' + house_id
                data = {
                    'house_id': house_id,
                    'url': detail_url
                }
                channel.queue_declare(queue='sold_price')
                channel.basic_publish(exchange='',
                                      routing_key='sold_price',
                                      body=json.dumps(data))
                print('放队列 {}'.format(data))

    def rent_house(self, second_category_url):
        """
        出租
        :param second_category_url:
        :return:
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbit']['host'],
                                                                       port=setting['rabbit']['port'],
                                                                       heartbeat=0))
        channel = connection.channel()
        total_page = self.get_max_page(second_category_url)
        rent_url = second_category_url.replace('realestateandhomes-search', 'apartments')
        for page in range(1, total_page + 1):
            page_url = rent_url + '/pg-' + str(page)
            print(page_url)
            r = requests.get(url=page_url, headers=self.headers)
            html = etree.HTML(r.text)
            house_list = html.xpath("//li[@class='component_property-card js-component_property-card js-quick-view']")
            for house in house_list:
                house_id = 'M' + house.xpath("./@data-propertyid")[0]
                detail_url = 'http://www.realtor.com/property-overview/' + house_id
                data = {
                    'house_id': house_id,
                    'url': detail_url
                }
                channel.queue_declare(queue='rent_price')
                channel.basic_publish(exchange='',
                                      routing_key='rent_price',
                                      body=json.dumps(data))
                print('放队列 {}'.format(data))

    def get_max_page(self, second_category_url):
        """
        获取最大页码
        :param second_category_url: 二级分类url
        :return:最大页码
        """
        r = requests.get(url=second_category_url, headers=self.headers)
        html = etree.HTML(r.text)
        page_info = html.xpath("//nav[@class='pagination']/span[@class='page']/a/text()")
        print(page_info)
        if len(page_info) > 0:
            a = []
            for i in page_info:
                a.append(int(i))
            total_page = max(a)
            print(total_page)
        else:
            total_page = 1
            print(total_page)
        return total_page


if __name__ == '__main__':
    url = 'https://www.realtor.com/realestateandhomes-search/Escambia-County_AL'
    c = Cookie(url)
    cookie = c.get_cookie()
    r = Realtor(cookie)
    r.start()



