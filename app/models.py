from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# People table (students and teachers)
class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # ✅ add this
    role = Column(String, nullable=False)
    hobbies = Column(Text, nullable=True)
    
    # Relationships
    credits = relationship('Credit', back_populates='person')
    subjects = relationship('PersonSubject', back_populates='person')
    hobbies_association = relationship('PersonHobby', back_populates='person')
    
# Hobbies table
class Hobby(Base):
    __tablename__ = 'hobbies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hobby_name = Column(String, unique=True, nullable=False)

    # Many-to-many relationship with Person
    people = relationship('PersonHobby', back_populates='hobby')

# Person-Hobby many-to-many table
class PersonHobby(Base):
    __tablename__ = 'person_hobbies'

    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    hobby_id = Column(Integer, ForeignKey('hobbies.id'), primary_key=True)

    person = relationship('Person', back_populates='hobbies_association')
    hobby = relationship('Hobby', back_populates='people')

# Terms table
class Term(Base):
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    # Relationship with subjects
    subjects = relationship('Subject', back_populates='term')

# Subjects table
class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    year_level = Column(Integer, nullable=True)  # Year level associated with the subject
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=True)
    teacher_id = Column(Integer, ForeignKey('people.id'), nullable=True)

    # Relationships
    term = relationship('Term', back_populates='subjects')
    teacher = relationship('Person')
    students = relationship('PersonSubject', back_populates='subject')

# Person-Subject many-to-many table
class PersonSubject(Base):
    __tablename__ = 'person_subjects'

    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)

    person = relationship('Person', back_populates='subjects')
    subject = relationship('Subject', back_populates='students')

# Credits table
class Credit(Base):
    __tablename__ = 'credits'

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    earned_credits = Column(Integer, nullable=False)
    required_credits = Column(Integer, nullable=False)

    # Relationships
    person = relationship('Person', back_populates='credits')
    subject = relationship('Subject')

# School Rules table
class SchoolRule(Base):
    __tablename__ = 'school_rules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_text = Column(Text, nullable=False)

# Database setup
DATABASE_URL = "sqlite:///school.db"  # Use your preferred database URL
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close()
