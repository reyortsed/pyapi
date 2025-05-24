from http import HTTPStatus
from fastapi import Depends, APIRouter, Request
from typing import List
from app.db.database import *
from app.db.request_context import *
from sqlalchemy import select, insert, delete, update 
from app.models import users
from app.schemas import CreateUserDTO, ReadUserDTO, UpdateUserDTO
from fastapi.responses import JSONResponse

router = APIRouter()

# GET /users/
@router.get("/users/", status_code=HTTPStatus.OK,response_model=List[ReadUserDTO])
async def read_users(request: Request, ctx: RequestContext = Depends()) -> List[ReadUserDTO]:
        stmt = select(users)
        result = await ctx.db.execute(stmt)
        rows = result.mappings().all()
        return [ReadUserDTO(**row) for row in rows]
   
# GET /users/{user_id}
@router.get("/users/{user_id}",status_code=HTTPStatus.OK,response_model=ReadUserDTO, )
async def read_user(user_id: int, ctx: RequestContext = Depends()):
    stmt = select(users).where(users.c.id == user_id)
    result = await ctx.db.execute(stmt)
    row = result.mappings().first()
    if not row:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": "User not found"}
        )
    return ReadUserDTO(**row)

# POST /users/
@router.post("/users/",status_code=HTTPStatus.OK, response_model=ReadUserDTO, ) # 200 because we return what was created
async def create_user(user_data: CreateUserDTO, ctx: RequestContext = Depends()):
    stmt = select(users).where(users.c.email == user_data.email)
    result = await ctx.db.execute(stmt)
    row = result.mappings().first()
    if row:
       return JSONResponse(
            status_code=HTTPStatus.CONFLICT,
            content={"detail": "User email ecists"}
        ) 
    
    stmt = insert(users).values(user_data.model_dump()).returning(users)
    result = await ctx.db.execute(stmt)
    await ctx.db.commit()
    row = result.mappings().first()
    return dict(row) if row else None

# PATCH /users/{user_id}
@router.patch("/users/{user_id}", status_code=HTTPStatus.OK, response_model=ReadUserDTO) # 200 because we return what was updated
async def update_user(user_id: int, updateUser: UpdateUserDTO, ctx: RequestContext = Depends()):
    # Filter out unset fields (only update what's submitted)
    user = updateUser.model_dump(exclude_unset=True)
    if not user:
        return None  # Nothing to update
    stmt = update(users).where(users.c.id == user_id).values(**user).returning(users)
    result = await ctx.db.execute(stmt)
    await ctx.db.commit()
    row = result.mappings().first()
    return dict(row) if row else None


# DELETE /users/{user_id}
@router.delete("/users/{user_id}", status_code=HTTPStatus.OK, response_model=ReadUserDTO) # 200 because we return what was deleted
async def delete_user(user_id: int, ctx: RequestContext = Depends()):
    stmt = (delete(users).where(users.c.id == user_id).returning(users))
    result = await ctx.db.execute(stmt)
    await ctx.db.commit()
    row = result.first() # Return what has been deleted
    if not row:
         return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"detail": "Could not delete, user not found"}
        )
    return dict(row) if row else None
