from sqlalchemy.sql.sqltypes import Integer, String, Text, Float, JSON
from sqlalchemy import Column
from app.db.database import Base


class Country(Base):
    __tablename__= "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capital = Column(String, nullable=False)
 

class Call(Base):
    __tablename__ = "calls"

    call_id = Column(String, primary_key=True, index=True)
    agent_id = Column(String)
    customer_name = Column(String)
    start_timestamp = Column(Integer)
    end_timestamp = Column(Integer)
    duration_ms = Column(Integer)
    call_summary = Column(Text)
    overall_sentiment = Column(String)
    transcript_object = Column(JSON)
