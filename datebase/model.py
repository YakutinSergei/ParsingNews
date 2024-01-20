from environs import Env
from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = Env()
env.read_env()


# Определение базового класса для объявления моделей
Base = declarative_base()

# Определение модели таблицы
class NewsTable(Base):
    __tablename__ = 'news_rhbz'

    id_news = Column(Integer, primary_key=True)
    title = Column(String(255))
    publish_date = Column(DateTime)
    content = Column(String)
    url = Column(String)


async def create_table(database_name=env('db_name'),
                 user=env('user'),
                 password=env('password'),
                 host=env('host'), port=5432):
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

def create_session(database_name=env('db_name'),
                 user=env('user'),
                 password=env('password'),
                 host=env('host'), port=5432):
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    return Session()


def add_news(title, publish_date, content, url):
    session = create_session()
    new_entry = NewsTable(title=title, publish_date=publish_date, content=content, url=url)
    session.add(new_entry)
    session.commit()
    session.close()


# Функция проверки есть ли такая новость
def news_exists(url):
    session = create_session()

    # Проверка наличия новости с заданным заголовком
    existing_news = (session.
                     query(NewsTable).
                     filter(func.lower(NewsTable.url) == func.lower(url)).first())
    session.close()

    return existing_news is not None