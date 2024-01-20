from datebase.model import create_table
import time
import datetime
import asyncio


from modul_parser_news.parsing_new import get_news_content_from_TASS
from modul_parser_news.ria_news import parce_ria



current_datetime = datetime.datetime.now()

# Получение текущего года, месяца, дня, часа, минут и секунд
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day
current_hour = current_datetime.hour
current_minute = current_datetime.minute
current_second = current_datetime.second


urls = ['https://www.mk.ru/rss/news/index.xml',
        'https://www.interfax.ru/rss.asp',
        'https://rssexport.rbc.ru/rbcnews/news/30/full.rss',
        'https://lenta.ru/rss/google-newsstand/main/',
        'https://aif.ru/rss/googlearticles',
        'http://www.vz.ru/export/yandex.xml',
        'http://www.rg.ru/xml/index.xml',
        'http://www.gazeta.ru/export/rss/social.xml',
        'http://russian.rt.com/rss/'
        ]

url_ria = (f'https://ria.ru/services/archive/widget/more.html?id=19180323&date={current_year}{current_month}{current_day}'
       f'T{current_hour}{current_minute}{current_second}&articlemask=lenta_common&type=lenta')





async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(create_table())
    while True:
        async with asyncio.TaskGroup() as tg:
            for url in urls:
                print(f'Новости с {url}')
                tg.create_task(get_news_content_from_TASS(url)) # Получаем новости РБК
            tg.create_task(parce_ria(url=url_ria))
        time.sleep(1800)

asyncio.run(main())

