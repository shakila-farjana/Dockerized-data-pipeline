import slack
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Float, String

oauth_token = ""

client = slack.WebClient(token=oauth_token)
#joke = pyjokes.get_joke()
HOST = 'mypg'
USERNAME = 'postgres'
PORT = '5432'
DB = 'postgres'
PASSWORD = '1234'

Base = declarative_base()
class Tweets(Base):
   __tablename__ = 'tweets'
   name = Column(String, primary_key =  True)
   text = Column(String)
   sentiment_score = Column(Float)
engine = create_engine(f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}')
Session = sessionmaker(bind = engine)
session = Session()
result = session.query(Tweets).all()
for row in result:
    texts = row.name + '\t' +row.text + '\t'+str(row.sentiment_score)
    response = client.chat_postMessage(channel='#botchannel', text=f"tweets: {texts}")
