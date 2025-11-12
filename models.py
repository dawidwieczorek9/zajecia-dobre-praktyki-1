from sqlalchemy import Column, Integer, String
from database import Base
import bcrypt


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="ROLE_USER")

    def verify_password(self, password: str):
        password_bytes = password.encode('utf-8')
        hashed_bytes = self.hashed_password.encode('utf-8')
        is_valid = bcrypt.checkpw(password_bytes, hashed_bytes)
        return is_valid
