from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

def add_news(session, title, publish_date, content, url):
    new_entry = NewsTable(title=title, publish_date=publish_date, content=content, url=url)
    session.add(new_entry)
    session.commit()