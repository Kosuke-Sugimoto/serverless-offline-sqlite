from sqlalchemy import create_engine
from sqlalchemy.schema import Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserData(Base):
    __tablename__ = "users"
    user_id = Column(String(255), primary_key=True)
    name = Column(String(255))
    age = Column(Integer)


if __name__=="__main__":
    engine = create_engine("sqlite:///users_offline.sqlite3", echo=True)

    Base.metadata.create_all(bind=engine)
    
    session = sessionmaker(bind=engine)()

    # Initial Data definition
    # for checking
    sample_user = UserData()
    sample_user.user_id = "0ada13"
    sample_user.name = "sample"
    sample_user.age = 100
    
    session.add(instance=sample_user)
    session.commit()
