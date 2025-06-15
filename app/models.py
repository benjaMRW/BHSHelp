from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from datetime import datetime

Base = declarative_base()

class Person(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "student" or "teacher"
    hobbies = Column(Text, nullable=True)
    
    # Relationships
    credits = relationship('Credit', back_populates='person')
    subjects = relationship('PersonSubject', back_populates='person')
    hobbies_association = relationship('PersonHobby', back_populates='person')
    liked_notices = relationship('LikedNotice', back_populates='person')
    feedbacks = relationship('Feedback', back_populates='person')

# Add these new models at the bottom of your existing models.py
class LikedNotice(Base):
    __tablename__ = 'liked_notices'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    notice_title = Column(String, nullable=False)
    notice_date = Column(String, nullable=False)
    liked_at = Column(DateTime, default=datetime.utcnow)
    
    person = relationship('Person', back_populates='liked_notices')

class Feedback(Base):
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('people.id'))
    idea = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_implemented = Column(Boolean, default=False)
    
    person = relationship('Person', back_populates='feedbacks')

# Initialize Database (keep your existing code)
engine = create_engine("sqlite:///school.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()