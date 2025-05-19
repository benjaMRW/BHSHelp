from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

# People table (students and teachers)
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

# Hobbies table
class Hobby(Base):
    __tablename__ = 'hobbies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hobby_name = Column(String, unique=True, nullable=False)
    people = relationship('PersonHobby', back_populates='hobby')

# Person-Hobby many-to-many table
class PersonHobby(Base):
    __tablename__ = 'person_hobbies'
    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    hobby_id = Column(Integer, ForeignKey('hobbies.id'), primary_key=True)
    person = relationship('Person', back_populates='hobbies_association')
    hobby = relationship('Hobby', back_populates='people')

# --------------------------
# Map-Related Tables
# --------------------------

# Blocks (letters: m, a, b, c, etc.)
class Block(Base):
    __tablename__ = 'blocks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    letter = Column(String(1), unique=True, nullable=False)  # Single char (e.g., 'm')
    name = Column(String)  # Optional: "Math Wing", "Arts Block"
    
    # Relationships
    subjects = relationship('Subject', back_populates='block')
    connected_locations = relationship('BlockLocation', back_populates='block')

# Locations (Cross Gym, Library, etc.)
class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String)  # "sports", "academic", "admin"
    
    # Relationships
    connected_blocks = relationship('BlockLocation', back_populates='location')

# Connects blocks to locations (many-to-many)
class BlockLocation(Base):
    __tablename__ = 'block_locations'
    block_id = Column(Integer, ForeignKey('blocks.id'), primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'), primary_key=True)
    distance = Column(Integer)  # Optional: walking distance in meters
    
    block = relationship('Block', back_populates='connected_locations')
    location = relationship('Location', back_populates='connected_blocks')

# --------------------------
# Academic Tables (Simplified)
# --------------------------

# Subjects (no term dependency)
class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.id'))  # Where it's taught
    teacher_id = Column(Integer, ForeignKey('people.id'))
    
    # Relationships
    block = relationship('Block', back_populates='subjects')
    teacher = relationship('Person')
    students = relationship('PersonSubject', back_populates='subject')

# Person-Subject many-to-many
class PersonSubject(Base):
    __tablename__ = 'person_subjects'
    person_id = Column(Integer, ForeignKey('people.id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), primary_key=True)
    person = relationship('Person', back_populates='subjects')
    subject = relationship('Subject', back_populates='students')

# Credits
class Credit(Base):
    __tablename__ = 'credits'
    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey('people.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    earned_credits = Column(Integer, nullable=False)
    required_credits = Column(Integer, nullable=False)
    person = relationship('Person', back_populates='credits')
    subject = relationship('Subject')

# School Rules
class SchoolRule(Base):
    __tablename__ = 'school_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_text = Column(Text, nullable=False)

# Initialize Database
engine = create_engine("sqlite:///school.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()