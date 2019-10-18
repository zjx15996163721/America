#!/usr/bin/env python3
from spider import Realtor
from get_cookie import Cookie
from consumer_sale_house import RealtorSaleHouseConsumer
from consumer_sold_house import RealtorSoldHouseConsumer
from consumer_rent_house import RealtorRentHouseConsumer


if __name__ == '__main__':
    """
    生产者将每个房源url放入队列，一共3种
    sale_house 挂牌出售
    sold_house 已经售出
    rent_house 出租
    """
    url = 'https://www.realtor.com/realestateandhomes-search/Escambia-County_AL'
    c = Cookie(url)
    cookie = c.get_cookie()
    r = Realtor(cookie)
    r.start()

    """
    消费者将消息从队列中取出根据id查询数据库
    """
    sale = RealtorSaleHouseConsumer()
    sale.start_consuming()

    sold = RealtorSoldHouseConsumer()
    sold.start_consuming()

    rent = RealtorRentHouseConsumer()
    rent.start_consuming()



