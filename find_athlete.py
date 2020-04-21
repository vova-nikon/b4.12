import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def connect_db():
    engine= sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def request_data():
    user_id = input("Enter your ID and I will find an athlete closest to you by their height \nand birth date! ")
    return int(user_id)

def convert_str_to_date(date_str):
    date_split = date_str.split("-")
    date_parts = map(int, date_split)
    date = datetime.date(*date_parts)
    return date

def closest_birthdate(user, session):
    athlete_list = session.query(Athelete).all()
    athlete_id_bd = {}
    for athlete in athlete_list:
        bd = convert_str_to_date(athlete.birthdate)
        athlete_id_bd[athlete.id] = bd

    user_bd = convert_str_to_date(user.birthdate)

    min_difference = None
    athlete_id = None
    athlete_bd = None

    for id_, bd in athlete_id_bd.items():
        difference = abs(user_bd - bd)
        if not min_difference or difference < min_difference:
            min_difference = difference
            athlete_id = id_
            athlete_bd = bd

    return athlete_bd, athlete_id

def closest_height(user, session):
    athlete_list = session.query(Athelete).filter(Athelete.height != None).all()
    athlete_id_ht = {}
    for athlete in athlete_list:
        athlete_id_ht[athlete.id] = athlete.height

    user_ht = user.height

    min_difference = None
    athlete_id = None
    athlete_ht = None

    for id_, ht in athlete_id_ht.items():
        if ht is None:
            continue

        difference = abs(user_ht - ht)
        if not min_difference or difference < min_difference:
            min_difference = difference
            athlete_id = id_
            athlete_ht = ht

    return athlete_ht, athlete_id

def main():
    session = connect_db()
    user_id = request_data()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print("There are no users with this ID")
    else:
        bd_athlete, bd = closest_birthdate(user, session)
        ht_athlete, ht = closest_height(user, session)
        print("The closest athlete by their birth date is the athlete with id {}. \nTheir birth date is: {}".format(bd_athlete, bd))
        print("The closest athlete by their height is the athlete with id {}. \nTheir height is: {}".format(ht_athlete, ht))

if __name__ == "__main__":
    main()