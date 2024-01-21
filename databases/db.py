from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

db = {}
Base = declarative_base()

def init_db(config):
    connection_engine = ("mysql+pymysql://{login}:{password}@{host}/{db}?charset=utf8mb4".format(**config))
    engine = create_engine(connection_engine)

    db["session"] = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    Base.query = db["session"].query_property()
    Base.metadata.create_all(bind=engine)
