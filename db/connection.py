from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(f'postgresql+psycopg2://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:5432/{os.environ["DB_NAME"]}')
# engine.echo = True 
conn = engine.connect()

Session = sessionmaker(engine)
session = Session()

