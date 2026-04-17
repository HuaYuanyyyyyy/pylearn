from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class ModelEntity(Base):
    __tablename__ = "ai_models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False)
    version = Column(String(20), nullable=False)
    parameter_size = Column(Float, nullable=False)
    is_deployed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())