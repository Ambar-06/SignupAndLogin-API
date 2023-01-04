from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class user_info(Base):
    __tablename__ = "users"
    name = Column(String)
    email = Column(String, unique=True, primary_key=True)
    password = Column(String)
    admin_account = Column(String)
    photo = Column(String)

    company = relationship("company_info", back_populates="employee_name")

class company_info(Base):
    __tablename__ = "companies"
    company = Column(String)
    employee_email = Column(String, ForeignKey("users.email"), primary_key=True)

    employee_name = relationship("user_info", back_populates="company")