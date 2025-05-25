#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Company, Dev, Freebie

if __name__ == '__main__':
    # Setup database engine and session
    engine = create_engine('sqlite:///freebies.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    

    #  1. Testing Dev's name and companies that gave them freebies
    dev = session.query(Dev).first()  # Get first dev or None
    if dev:
        print(f"Dev: {dev.name}")
        print("Companies that gave freebies to this dev:")
        for company in dev.companies:
            print(f"  - {company.name}")
    else:
        print("No Dev found in database.")

    # 2.Testing Company name and devs who received freebies from them
    company = session.query(Company).first()  # Get first company or None
    if company:
        print(f"Company: {company.name}")
        print("Devs who got freebies from this company:")
        for dev in company.devs:
            print(f"  - {dev.name}")
    else:
        print("No Company found in database.")

    # 3. esting which freebie was given to who and by which company
    freebie = session.query(Freebie).first()
    if freebie:
        print(f"Freebie: {freebie.item_name}, value: {freebie.value}")
        print(f"Given by: {freebie.company.name if freebie.company else 'Unknown company'}")
        print(f"Received by: {freebie.dev.name if freebie.dev else 'Unknown dev'}")
    else:
        print("No Freebie found in database.")


     # 4. Test give_freebie (Company creates a new freebie)
    print("\nTesting Company.give_freebie()...")
    new_freebie = company.give_freebie(dev, "umbrella", 10)
    session.add(new_freebie)
    session.commit()
    print(f"Created new freebie: {new_freebie.print_details()}")

    # 5. Test Company.oldest_company()
    print("\nTesting Company.oldest_company()...")
    oldest = Company.oldest_company(session)
    print(f"Oldest Company: {oldest.name}, Founded: {oldest.founding_year}")

    # 6. Test Dev.received_one()(The dev that received the item)
    print("\nTesting Dev.received_one('umbrella')...")
    print(f"Received 'umbrella? {dev.received_one('umbrella')}")


    # Used as an interactive debugger
    import ipdb; ipdb.set_trace()
    
