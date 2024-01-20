from bs4 import BeautifulSoup
import requests
import datetime
import asyncio


from datebase.model import news_exists, add_news
from modul_parser_news.parsing_new import contains_word

# Определение заголовков, которые будут отправлены с запросом
headers = {
    'User-Agent': 'Mozilla/5.0',                  # Идентификация типа браузера, который отправляет запрос
    'Accept': 'text/html,application/xhtml+xml',  # Типы контента, которые клиент может обработать
    'Connection': 'keep-alive'                    # Указание на необходимость использования постоянного соединения
}

current_datetime = datetime.datetime.now()

# Получение текущего года, месяца, дня, часа, минут и секунд
current_year = current_datetime.year
current_month = current_datetime.month
current_day = current_datetime.day
current_hour = current_datetime.hour
current_minute = current_datetime.minute
current_second = current_datetime.second


start_urls = 'https://ria.ru'

file_path = 'stop_word.txt'

# Открываем файл для чтения
with open(file_path, 'r', encoding='utf-8') as file:
    # Считываем строки из файла и создаем список
    lines = [line.strip() for line in file if line.strip()]


async def parce_ria(url, offset = 0, status = 0):
    if status == 0:
        response = requests.get(url=url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        links = soup.find_all('a', class_='lenta__item-size')
        texts = soup.find_all('span', class_='lenta__item-text')
        urls = [link.get('href') for link in links if link.get('href')]
        times_news = soup.find_all('span', class_='lenta__item-date')


        for i in range(offset, len(urls)): # Перебераем все ссылки
            if not news_exists(start_urls + urls[i]): # Проверяем есть ли такая ссылка базе данных, если нет
                response = requests.get(url=start_urls + urls[i], headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                article = soup.find('div', class_='layout-article__main-over').find_all('div', class_='article__text')
                papers = [text.text for text in article]
                paper = ''
                for text in papers:
                    paper += text



                count, matching_words = contains_word(paper, lines)
                if matching_words:
                    # Время и дата публикации статьи
                    time_date_news = soup.find('div', class_='article__info-date').text
                    date_object = datetime.datetime.strptime(time_date_news, "%H:%M %d.%m.%Y")

                    # Форматирование объекта datetime в нужную строку
                    time_date_news = date_object.strftime("%Y-%m-%d %H:%M:%S")

                    print(f'ЗАГОЛОВОК: {texts[i].text}\n'
                                  f'Статья: {paper}\n'
                                  f'Ссылка: {start_urls+urls[i]}\n'
                                  f'Время: {times_news[i].text}\n')
                    print(f"Количество совпадающих слов: {count}")
                    print(f"Совпадающие слова: {matching_words}")
                    add_news(texts[i].text, time_date_news, paper, start_urls + urls[i])

            else: # Если есть такая ссылка, то прерываем цикл
                status = 1
                break

        date_end = urls[19].split("/")[1]
        time_hours_end = times_news[19].text.split(':')[0]
        time_minutes_end = times_news[19].text.split(':')[1]
        date_end_news = datetime.datetime.strptime(f'{date_end}{time_hours_end}{time_minutes_end}', "%Y%m%d%H%M")

        time_difference = current_datetime - date_end_news

        if time_difference < datetime.timedelta(days=1):
            url = (
                f'https://ria.ru/services/archive/widget/more.html?id=19180323&date={date_end}'
                f'T{time_hours_end}{time_minutes_end}{current_second}&articlemask=lenta_common&type=lenta')
            await parce_ria(url=url, offset=1, status=status)
