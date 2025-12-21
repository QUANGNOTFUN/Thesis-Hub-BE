from sqlmodel import SQLModel

from app.core.database import engine
from app.features.auth import models as auth_models  # noqa: F401


def create_tables():
    SQLModel.metadata.create_all(bind=engine)
    print("Created tables")


if __name__ == "__main__":
    create_tables()
