import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.Text)
	last_name = sa.Column(sa.Text)
	gender = sa.Column(sa.Text)
	email = sa.Column(sa.Text)
	birthdate = sa.Column(sa.Text)
	height = sa.Column(sa.REAL)

def connect_db():
	engine= sa.create_engine(DB_PATH)
	Base.metadata.create_all(engine)
	session = sessionmaker(engine)
	return session()

def request_data():
	first_name = input("Please enter your first name: ")
	last_name = input("Please enter your last name: ")
	gender = input("Please enter your gender (Male / Female): ")
	email = input("Please enter your email: ")
	birthdate = input("Please enter your birth date (YYYY-MM-DD): ")
	height = input("Please enter your height (1.70 / 1.56 / 1.93): ")
	user = User(
		first_name=first_name,
		last_name=last_name,
		gender=gender,
		email=email,
		birthdate=birthdate,
		height=height
		)
	return user

def main():
	session = connect_db()
	print("Hello, I will create a new user with your data!")
	user = request_data()
	session.add(user)
	session.commit()
	print("Your data has been saved, thank you!")

if __name__ == "__main__":
	main()