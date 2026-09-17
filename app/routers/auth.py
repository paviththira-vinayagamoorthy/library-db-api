from fastapi import (
   APIRouter,
   Depends,
   HTTPException,
   status
)


from fastapi.security import (
   OAuth2PasswordRequestForm
)


from sqlalchemy.orm import Session


from app.database.connection import get_db  # அல்லது app.database.database
from app.models.user import User
from app.schemas.user import UserRegister, UserResponse, Token
from app.auth.security import authenticate_user, create_access_token, get_current_user, hash_password


router = APIRouter(
   prefix="/auth",
   tags=["Authentication"]
)


@router.post(
   "/register",
   response_model=UserResponse,
   status_code=status.HTTP_201_CREATED
)
def register_user(
   user_data: UserRegister,
   db: Session = Depends(get_db)
):
   existing_username = (
       db.query(User)
       .filter(
           User.username == user_data.username
       )
       .first()
   )


   if existing_username:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Username already exists"
       )


   existing_email = (
       db.query(User)
       .filter(
           User.email == user_data.email
       )
       .first()
   )


   if existing_email:
       raise HTTPException(
           status_code=status.HTTP_400_BAD_REQUEST,
           detail="Email already exists"
       )


   new_user = User(
       username=user_data.username,
       email=user_data.email,
       full_name=user_data.full_name,


       hashed_password=hash_password(
           user_data.password
       ),


       role="Member",
       active=True
   )


   db.add(new_user)
   db.commit()
   db.refresh(new_user)


   return new_user


@router.post(
   "/login",
   response_model=Token
)
def login(
   form_data: OAuth2PasswordRequestForm = Depends(),
   db: Session = Depends(get_db)
):
   user = authenticate_user(
       db,
       form_data.username,
       form_data.password
   )


   if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Incorrect username or password",
           headers={
               "WWW-Authenticate": "Bearer"
           }
       )


   if not user.active:
       raise HTTPException(
           status_code=status.HTTP_403_FORBIDDEN,
           detail="Inactive user"
       )


   access_token = create_access_token(
       data={
           "sub": user.username
       }
   )


   return {
       "access_token": access_token,
       "token_type": "bearer"
   }
@router.get(
   "/me",
   response_model=UserResponse
)
def get_my_profile(
   current_user: User = Depends(
       get_current_user
   )
):
   return current_user




