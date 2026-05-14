from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Integer, Float, DateTime, Boolean

from uuid import uuid4
import uuid as uuid_pkg 
from sqlalchemy.dialects.postgresql import UUID


from datetime import datetime, timezone

from api.v1.database.session import Base 



class UserTable(Base):
    
    __tablename__ = "users"          

    id: Mapped[uuid_pkg.UUID] = mapped_column(
                    UUID(as_uuid=True),   
                    primary_key=True,
                    default=uuid4
    )
    
    username : Mapped[str] = mapped_column(String(50),   
                                           unique=True, 
                                           nullable=False, 
                                           index=True
                                           )

    hashed_password : Mapped[str] = mapped_column(String(255),
                                                  nullable=False
                                                 )

    is_active : Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


    created_at : Mapped[datetime] = mapped_column(DateTime,
                                                  default = datetime.utcnow, 
                                                  nullable=False)
    

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"



