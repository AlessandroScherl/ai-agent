from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, DateTime


def get_utc_now():
    return datetime.now().replace(tzinfo=timezone.utc)

class ChatMessagePayload(SQLModel):
    # pydantic model for validaiton and serializer
    message: str

class ChatMessage(SQLModel, table=True):
    # db table
    # saving, updating, getting, deleting
    id: int | None = Field(default=None, primary_key=True) # 1, 2, 3, 4 ...
    message: str
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=DateTime(timezone=True), # based on sqlalchmy
        primary_key=False,
        nullable = False,

    )
    # in longrun e.g. "alembic" for changes to DB model

class ChatMessageListItem(SQLModel):
    id: int | None = Field(default=None)
    message: str
    created_at: datetime = Field(default=None)
