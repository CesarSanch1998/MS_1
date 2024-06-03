from psycopg import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()

engine = create_engine(f'postgresql+psycopg://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}@{os.environ["DB_HOST"]}:5432/{os.environ["DB_NAME"]}')
engine.echo = True 
try:
    conn = engine.connect()
except OperationalError as e:
    print(f"Error de conexión a la base de datos: {e}")

Session = sessionmaker(engine)
session = Session()

