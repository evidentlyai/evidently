from sqlalchemy import create_engine

from config import MONITORING_DB_URI
from src.utils.models import Base

if __name__ == "__main__":
    engine = create_engine(MONITORING_DB_URI)
    Base.metadata.drop_all(engine)
    print("Database dropped successfully")
