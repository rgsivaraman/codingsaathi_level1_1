from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


# Association table for agent collaborators
agent_collaborators = Table(
    'agent_collaborators',
    Base.metadata,
    Column('agent_id', Integer, ForeignKey('agents.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agents = relationship("Agent", back_populates="creator", foreign_keys="Agent.creator_id")
    ratings = relationship("Rating", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    collaborating_agents = relationship("Agent", secondary=agent_collaborators, back_populates="collaborators")


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    code = Column(Text, nullable=False)
    tags = Column(String)  # Comma-separated tags
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)  # For forked agents
    version = Column(String, default="1.0.0")
    is_public = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="agents", foreign_keys=[creator_id])
    parent = relationship("Agent", remote_side=[id], backref="forks")
    ratings = relationship("Rating", back_populates="agent", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="agent", cascade="all, delete-orphan")
    collaborators = relationship("User", secondary=agent_collaborators, back_populates="collaborating_agents")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 stars
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="ratings")
    user = relationship("User", back_populates="ratings")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent = relationship("Agent", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
