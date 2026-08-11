import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Prompt(Base):
    __tablename__ = "prompts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_text = Column(Text, nullable=False)
    task_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    evaluations = relationship("Evaluation", back_populates="prompt")
    improvements = relationship("Improvement", back_populates="prompt")


class Evaluation(Base):
    __tablename__ = "evaluations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"))
    dimension = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    reasoning = Column(Text, nullable=True)
    missing_elements = Column(JSON, nullable=True)
    model_used = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    prompt = relationship("Prompt", back_populates="evaluations")


class Improvement(Base):
    __tablename__ = "improvements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"))
    improved_text = Column(Text, nullable=False)
    # "rule_based" or "meta_prompt"
    strategy_used = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    prompt = relationship("Prompt", back_populates="improvements")
