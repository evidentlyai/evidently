from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# [Prediction]

class PredictionTable(Base):
    """Implement table for storing features with corresponding predictions."""

    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True)
    lpep_pickup_datetime = Column(Float)
    PULocationID = Column(Integer)
    DOLocationID = Column(Integer)
    passenger_count = Column(Integer)
    trip_distance = Column(Float)
    fare_amount = Column(Float)
    total_amount = Column(Float)
    uuid = Column(String)
    duration_min = Column(Float)
    predictions = Column(Float)
