from config import MONITORING_DB_URI
from sqlalchemy import create_engine
from src.utils.models import Base

if __name__ == "__main__":
    engine = create_engine(MONITORING_DB_URI)
    Base.metadata.create_all(engine)
    print("Database created successfully")
