from newspaper import Article
import feedparser
import random
import time
import asyncio


from datebase.model import add_news, news_exists

file_path = 'stop_word.txt'

# Открываем файл для чтения
with open(file_path, 'r', encoding='utf-8') as file:
    # Считываем строки из файла и создаем список
    lines = [line.strip() for line in file if line.strip()]


async def get_news_content_from_TASS(url_rss): # Получаем ссылки на новости из RSS
    feed = feedparser.parse(url_rss)
    print('тиу')
    if feed.bozo:
        print("Error parsing the feed:", feed.bozo_exception)
        return

    for entry in feed.entries:
        url_news = entry.link
        pub_date = entry.published
        new = get_news_content(url_news, pub_date)
        if new:
            break
        print('Новость обработана')
        delay = random.uniform(3, 7)  # Случайная задержка от 3 до 7 секунд
        await asyncio.sleep(delay)


def get_news_content(url, pub_date):
    article = Article(url)
    article.download()
    article.parse()

    title = article.title
    content = article.text

    print("Title:", title) # Заголовок
    print("Publish Date:", pub_date) # Дата опубликования
    print("Content:", content) # Текст новости
    print("URL:", url) # Ссылка на новость
    print("-" * 30)
    if not news_exists(url): # Проверяем есть ли такая новость
        count, matching_words = contains_word(content, lines)
        if matching_words:
            print("Content:", content) # Текст новости
            print(f"Количество совпадающих слов: {count}")
            print(f"Совпадающие слова: {matching_words}")
            add_news(title, pub_date, content, url)
        else:
            return 0
    else:
        return 1




# функция проверки слов
def contains_word(text, word_list):
    # Переводим все слова в нижний регистр для регистронезависимого сравнения
    text_lower = text.lower()
    word_list_lower = [word.lower() for word in word_list]

    # Ищем совпадающие слова и подсчитываем их количество
    matching_words = [word for word in word_list_lower if word in text_lower]
    matching_words_count = len(matching_words)

    return matching_words_count, matching_words