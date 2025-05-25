#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Dev, Company, Freebie

#create an engine connected to my SQlite database

engine=create_engine('sqlite:///freebies.db')

#this creates all tables in the database if they do not exist

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
#create a configured session's class

session=Session()

#creating sample companies

company1=Company(name='Melldee', founding_year=2019)
company2=Company(name='TooGood', founding_year=2010)

#this adds the created companies above to the Session so that they are added to the database

session.add_all([company1, company2])

#sample of devs

dev1= Dev(name='Ruth')
dev2= Dev(name='Ken')

session.commit() #commiting so that ids for both companies and dev get assigned in the database

#create sample of freebies and link them with dev and companies using foreign keys

first_freebie=Freebie(item_name='mug', value=2, dev=dev1, company=company2)
second_freebie=Freebie(item_name='t-shirt', value=3, dev=dev2, company=company1)
third_freebie=Freebie(item_name='umbrella', value=1, dev=dev1, company=company2)


#add freebies to session

session.add_all([first_freebie, second_freebie, third_freebie])

#commit all changes

session.commit()

print("Seed info inserted successfully!")