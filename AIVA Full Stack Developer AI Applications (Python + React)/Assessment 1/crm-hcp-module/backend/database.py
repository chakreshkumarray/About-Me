"""Database configuration and models for CRM-HCP module"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost/crm_hcp_db")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Database Models
class HCP(Base):
    """Healthcare Provider model"""
    __tablename__ = "hcps"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String(50), unique=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100))
    license_number = Column(String(50))
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with interactions
    interactions = relationship("Interaction", back_populates="hcp")

class Interaction(Base):
    """HCP Interaction model"""
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    interaction_type = Column(String(50))  # meeting, call, email, etc.
    notes = Column(Text)
    sentiment = Column(String(20))  # positive, neutral, negative
    samples_provided = Column(String(255))  # comma-separated sample names
    follow_up_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with HCP
    hcp = relationship("HCP", back_populates="interactions")

class AIInsight(Base):
    """AI-generated insights model"""
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    hcp_id = Column(Integer, ForeignKey("hcps.id"))
    insight_type = Column(String(50))  # recommendation, summary, alert
    content = Column(Text)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

# Initialize database
def init_db():
    """Initialize database with sample data"""
    create_tables()

    # Create session
    db = SessionLocal()
    try:
        # Check if sample data exists
        if not db.query(HCP).first():
            # Create sample HCP
            sample_hcp = HCP(
                provider_id="HCP001",
                name="Dr. Sarah Johnson",
                specialization="Cardiology",
                license_number="MD123456",
                email="sarah.johnson@hospital.com",
                phone="+1-555-0123"
            )
            db.add(sample_hcp)
            db.commit()
            db.refresh(sample_hcp)

            # Create sample interaction
            sample_interaction = Interaction(
                hcp_id=sample_hcp.id,
                interaction_type="meeting",
                notes="Discussed new cardiac medication options",
                sentiment="positive",
                samples_provided="CardioMed A, CardioMed B"
            )
            db.add(sample_interaction)
            db.commit()

        print("Database initialized with sample data")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()