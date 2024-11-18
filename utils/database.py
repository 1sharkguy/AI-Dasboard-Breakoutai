from sqlalchemy import create_engine, Column, Integer, String, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.config import DATABASE_URI

# SQLAlchemy setup
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define your table(s)
class UploadedData(Base):
    __tablename__ = 'uploaded_data'
    id = Column(Integer, primary_key=True, index=True)
    column_name = Column(String, index=True)
    preview_data = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)
