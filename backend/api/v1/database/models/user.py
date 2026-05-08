from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String, Integer, Float, DateTime, Boolean

from datetime import datetime 

from api.v1.database.session import Base 
import uuid



class UserTable(Base):
    id : Mapped[uuid.UUID] = mapped_column(uuid.UUID(as_uuid=True),
                                           primary_key=True,
                                           index=True, 
                                           default=uuid.uuid4)
    
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
                                                  default=datetime.now(datetime.UTC), 
                                                  nullable=False)
    

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"



