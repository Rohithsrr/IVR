from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


class IVRScenario(Base):
    __tablename__ = "ivr_scenarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    scenario_type: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    steps = relationship("IVRStep", back_populates="scenario", cascade="all, delete-orphan")


class IVRStep(Base):
    __tablename__ = "ivr_steps"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("ivr_scenarios.id"), nullable=False)
    step_key: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, default="")
    options_json: Mapped[str] = mapped_column(Text, default="{}")
    fallback_key: Mapped[str] = mapped_column(String(100), default="")
    transfer_target: Mapped[str] = mapped_column(String(100), default="")
    final_outcome: Mapped[str] = mapped_column(String(255), default="")
    scenario = relationship("IVRScenario", back_populates="steps")


class Call(Base):
    __tablename__ = "calls"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acs_call_connection_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("ivr_scenarios.id"), nullable=False)
    from_number: Mapped[str] = mapped_column(String(50), default="")
    to_number: Mapped[str] = mapped_column(String(50), default="")
    direction: Mapped[str] = mapped_column(String(50), default="outbound")
    status: Mapped[str] = mapped_column(String(50), default="initiated")
    current_step_key: Mapped[str] = mapped_column(String(100), default="start")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CallEvent(Base):
    __tablename__ = "call_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[int] = mapped_column(ForeignKey("calls.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    payload: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CallResult(Base):
    __tablename__ = "call_results"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_id: Mapped[int] = mapped_column(ForeignKey("calls.id"), nullable=False)
    outcome: Mapped[str] = mapped_column(String(255), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
