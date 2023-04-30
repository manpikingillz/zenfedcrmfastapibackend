import os
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models.schemas.user import Token, TokenData, UserModel, UserInDB
from app.models.sql.user import User
from app.models.sql.user import get_user
from datetime import datetime, timedelta
from typing import Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.database.session import get_db
from datetime import timezone
from sqlalchemy.orm import Session

from dotenv import load_dotenv

load_dotenv()

# to get a string like this run:
# openssl rand -hex 32

# JWT_SECRET_KEY and JWT_REFRESH_SECRET_KEY can be any strings,
# but make sure to keep them secret and set them as environment variables.
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY')

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter()

# ####### Utils for verifying and hasshing passwoord
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Takes the plain and hashed passwords and return a boolean
    representing whether the passwords match or not.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Takes a plain password and returns the hash for
    it that can be safely stored in the database
    """
    return pwd_context.hash(password)
# ####### End of tils for verifying and hasshing passwoord


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create an access token for the given user.

    Returns:
    - A JWT access token string that can be used to
    authenticate the user in subsequent requests.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a refresh token for the given user.

    Returns:
    - A JWT refresh token string that can be used to refresh the access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user(username: str, plain_password: str, db: Session):
    """
    Authenticate user by checking if the username and password match.
    """
    if user := get_user(username=username, db=db):
        return user if verify_password(
            plain_password, user.password) else False
    else:
        return False


# USER LOGIN ------------------------------------------------------
@router.post("/token", response_model=Token)
async def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Access Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Refresh Token
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
        }


# USER SIGNUP ------------------------------------------------------
@router.post('/signup', summary="Create new user", response_model=UserModel)
async def create_user(create_user: UserModel,  db: Session = Depends(get_db)):

    # querying database to check if user already exist
    user = db.query(User).filter(User.username == create_user.username).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    hashed_password = get_password_hash(create_user.password)
    db_user = User(full_name=create_user.full_name,
                   email=create_user.email,
                   username=create_user.username,
                   password=hashed_password,
                   disabled=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {'message': "User created successfully"}


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserModel, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.get("/users/me/", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)]
):
    return current_user
