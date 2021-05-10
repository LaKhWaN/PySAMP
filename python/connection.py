from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==================== [ TABLE CREATION AND OTHER THINGS ] ================== #

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    admin_level = Column(Integer,default=0)

engine = create_engine("sqlite:///roleplay.db",echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session  = Session()