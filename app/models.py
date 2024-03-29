from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default='True',nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    owner = relationship('User')

class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Votes(Base):
    __tablename__='votes'
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True)