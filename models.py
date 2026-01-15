from flask_security.models import fsqla_v3 as fsqla
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import *
from sqlalchemy import ForeignKey, Column, Enum


db = SQLAlchemy()

# Define models
fsqla.FsModels.set_db_info(db)

class Role(db.Model, fsqla.FsRoleMixin):
    pass

class User(db.Model, fsqla.FsUserMixin):
    pass

class Computer(db.Model):
    pc_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str]
    hostname: Mapped[str]
    platform: Mapped[str] = Column(Enum("Windows", "Linux", "MacOS"))
    os: Mapped[str]
    ram: Mapped[int]
    cpu_cores: Mapped[int]
    cpu_architecture: Mapped[str]
    cpu_name: Mapped[str]

    blocked_websites: Mapped[list["Blocked_websites"]] = relationship(back_populates="computer", cascade="all, delete-orphan")


class Blocked_websites(db.Model):
    pc_id: Mapped[str] = mapped_column(ForeignKey("computer.pc_id"), primary_key=True)
    url: Mapped[str] = mapped_column(primary_key=True)
    computer: Mapped["Computer"] = relationship(back_populates="blocked_websites")
