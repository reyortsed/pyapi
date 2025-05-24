from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
#from typing import Any 
from app.db.database import get_db
#from auth import get_current_user

class RequestContext:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db)
        #,_: Any = Depends(get_current_user)
    ):
        self.db = db
