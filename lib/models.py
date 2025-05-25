from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship,backref
from sqlalchemy.orm import declarative_base


# Define a naming convention for database constraints, helpful for migrations
convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
# Use this naming convention in the metadata
metadata = MetaData(naming_convention=convention)

# Create a base class for our models, using the custom metadata
Base = declarative_base(metadata=metadata)



# Company model represents companies that give out freebies
class Company(Base):
    __tablename__ = 'companies'  # Name of the table in the database


    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    # Relationship to Freebie model - a company has many freebies
    # back_populates links this to the 'company' attribute in Freebie
    freebies = relationship("Freebie", back_populates="company")

    #want to know which devs have gotten the freebies from the company
    @property
    def devs(self):
        return list({freebie.dev for freebie in self.freebies if freebie.dev})


    def give_freebie(self , dev, item_name, value):
        #returns a new instance of a freebie connected to the company and the dev who got it
        new_freebie=Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return new_freebie
        session.commit()

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()    

    def __repr__(self):
        # String representation for debugging 
        return f'<Company {self.name}>'


class Dev(Base):
    __tablename__ = 'devs'  # Table name in DB

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Relationship to Freebie model - a dev has many freebies
    # back_populates links this to the 'dev' attribute in Freebie
    freebies = relationship("Freebie", back_populates="dev")

    @property
    def companies(self):
        #returns a list of companies the dev has gotten the freebies from
        return list({freebie.company for freebie in self.freebies if freebie.company})

    

    def received_one(self, item_name):
        # Returns True if this dev has a freebie with the given item name
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        # Transfers the freebie to another dev only if this dev owns it
        if freebie in self.freebies:
            freebie.dev = other_dev    
    

    def __repr__(self):
        return f'<Dev {self.name}>'


# Freebie model represents the freebies items obtained by devs from companies
class Freebie(Base):
    __tablename__ = 'freebies'  # Table name in DB

    # Primary key column - unique id for each freebie
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)

    # Foreign key to link to dev who owns the freebie
    dev_id = Column(Integer, ForeignKey('devs.id'))

    # Foreign key to link to company that gave the freebie
    company_id = Column(Integer, ForeignKey('companies.id'))

    # Relationship attribute to access the Dev object for this freebie
    # back_populates links this to the 'freebies' attribute in Dev
    dev = relationship("Dev", back_populates="freebies")

    # Relationship attribute to access the Company object for this freebie
    # back_populates links this to the 'freebies' attribute in Company
    company = relationship("Company", back_populates="freebies")

    def print_details(self):
        return f"{self.dev.name}, was awarded {self.item_name} by {self.company.name}"

    def __repr__(self):
        return f'<Freebie {self.item_name} - Value: {self.value}>'

if __name__ == '__main__':
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///freebies.db')
    Base.metadata.create_all(engine)