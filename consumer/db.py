from sqlmodel import create_engine
from env_vars import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)