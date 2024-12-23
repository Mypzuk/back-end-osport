from sqlalchemy import Integer, String, Float, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)  # Новое поле
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
    sex: Mapped[str] = mapped_column(String(1), nullable=True)
    weight: Mapped[str] = mapped_column(String,nullable=True )
    height: Mapped[str] = mapped_column(String,nullable=True )
    total_experience: Mapped[float] = mapped_column(Float, default=0, nullable=True)
    current_experience: Mapped[float] = mapped_column(Float, default=0, nullable=True)





    results: Mapped["Results"] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class Competitions(Base):
    __tablename__ = "competitions"

    competition_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=True)
    coefficient: Mapped[float] = mapped_column(Float, nullable=True)
    video_instruction: Mapped[str] = mapped_column(String, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, default=func.now(), nullable=False) 
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[Date] = mapped_column(String, default="free")

    results: Mapped["Results"] = relationship(
        back_populates="competition", cascade="all, delete-orphan"
    )

class Results(Base):
    __tablename__ = "results"

    result_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    competition_id: Mapped[int] = mapped_column(
        ForeignKey(Competitions.competition_id, ondelete="CASCADE"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(Users.id, ondelete="CASCADE"),
        nullable=False
    )

    video: Mapped[str] = mapped_column(String, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(1), nullable=False)

    competition: Mapped["Competitions"] = relationship(
        back_populates="results"
    )

    user: Mapped["Users"] = relationship(
        back_populates="results"
    )
    


class Whitelist(Base):
    __tablename__ = "whitelist"


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    competition_id: Mapped[int] = mapped_column(
        ForeignKey(Competitions.competition_id, ondelete="CASCADE"),
        nullable=False
    )
    email: Mapped[str] = mapped_column(String(100), nullable=False)
