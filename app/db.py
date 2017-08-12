from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    chain = Column(String)
    token_address = Column(String)
    library_address = Column(String)

    def __repr__(self):
        return 'chain: {}\nToken Contract: {}'.format(
            self.chain, self.token_address)


class DB():
    def __init__(self):
        self.engine = create_engine('sqlite:///core.db', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_all(self):
        Base.metadata.create_all(self.engine)
