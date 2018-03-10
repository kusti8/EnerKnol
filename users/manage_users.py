from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.apps import custom_app_context as pwd_context # Used for hashing
from create_user_database import User, Base

class ManageUsers():
    def __init__(self): # Connect to the database
        eng = create_engine('sqlite:///users.db')

        Base.metadata.bind = eng

        Session = sessionmaker(bind=eng)
        self.ses = Session()

    def add_user(self, added_user): # Abstraction to add user
        if self.ses.query(User).filter(User.Username == added_user.Username).one_or_none() is not None:  # Check if there already exists a username
            return False
        added_user.Password = pwd_context.hash(added_user.Password)
        self.ses.add(added_user)
        self.ses.commit()
        return True
    
    def login_user(self, username, password): # Login the user. Returns True if successful
        queried_user = self.ses.query(User).filter(User.Username == username).one_or_none() # We assume there is one username
        if queried_user is None: # username not found
            return False
        return pwd_context.verify(password, queried_user.Password) # Return whether the hashes match