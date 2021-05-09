from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import hashlib


Base = declarative_base()

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    name = Column(String(24), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

engine = create_engine("sqlite:///roleplay.db",echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(engine)
session  = Session()

def IsPlayerRegistered(playerid):
    print("================================================================")
    print(session.query(Player.name).filter(Player.name == "Upender_Lakhwan"))
    if(session.query(Player.name).filter(Player.name == "Upender_Lakhwan").count() and playerid == 1):
        return True
    else:
        return False

playerid = 1
if(IsPlayerRegistered(playerid)):
    password = input("Enter your password here: ")
    sql_password = session.query(Player.password).filter(Player.name == "Upender_Lakhwan").one_or_none()[0]
    print(sql_password)
    if(hashlib.sha256(password.encode()).hexdigest() == sql_password):
        print("Correct Passsword")
    else:
        print("Incorrect password")
else:
    passwd = input("You aren't registered, please enter your new password: ")
    password_new = hashlib.sha256(passwd.encode()).hexdigest()
    print(password_new)
    playerid = Player(name="Upender_Lakhwan",password=password_new)
    session.add(playerid)
    session.commit()
    print("Registered.")