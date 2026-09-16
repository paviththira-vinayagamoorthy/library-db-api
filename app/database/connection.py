from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    query={
        "charset": "utf8mb4"
    }
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

# get_db ஃபங்ஷனை Base கிளாஸுக்கு வெளியே, சரியான இடைவெளியுடன் எழுத வேண்டும்
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()