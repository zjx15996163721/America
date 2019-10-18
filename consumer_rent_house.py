#!/usr/bin/env python3
import pika
import yaml
import json
from pymongo import MongoClient
import requests
setting = yaml.load(open('config.yaml'))
m = MongoClient(host=setting['mongo']['host'], port=setting['mongo']['port'], username=setting['mongo']['user_name'], password=setting['mongo']['password'])
collection = m[setting['mongo']['db_name']][setting['mongo']['collection3']]


class RealtorRentHouseConsumer:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbit']['host'],
                                                                            port=setting['rabbit']['port'],
                                                                            heartbeat=0))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='rent_price')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }

    def parse(self, data):
        house_id = data['house_id']
        detail_url = data['url']
        # https://www.realtor.com/property-overview/M8858371726
        if not collection.find_one({'house_id': house_id}):
            self.get_house_info(detail_url)
        else:
            print('重复数据')

    def get_house_info(self, detail_url):
        r = requests.get(url=detail_url, headers=self.headers)
        property = r.json()['property']
        house_id = property['property_id']
        city = property['city']
        state = property['state']
        county = property['county']
        status = property['status']
        lat = property['lat']
        long = property['long']
        address = property['address']
        type_display = property['type_display']
        beds = property['beds']
        price = property['price']
        description = property['description']
        photos = property['photos']
        photos_list = []
        for photo in photos:
            photo_url = photo['url']
            photos_list.append(photo_url)

        data = {
            'house_id': house_id,
            'city': city,
            'state': state,
            'county': county,
            'status': status,
            'lat': lat,
            'long': long,
            'address': address,
            'type_display': type_display,
            'beds': beds,
            'price': price,
            'description': description,
            'photos': photos_list
        }
        collection.insert_one(data)
        print('存入一条数据{}'.format(data))

    def callback(self, ch, method, properties, body):
        data = json.loads(body.decode())
        self.parse(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback, queue='rent_price')
        self.channel.start_consuming()


