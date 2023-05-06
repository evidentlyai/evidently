from config.db_config import DATABASE_URI
from sqlalchemy import create_engine
from src.utils.models import Base

if __name__ == "__main__":
    engine = create_engine(DATABASE_URI)
    Base.metadata.drop_all(engine)
