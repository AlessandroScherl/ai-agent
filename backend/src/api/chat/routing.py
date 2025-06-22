from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.db import get_session
from .models import ChatMessagePayload, ChatMessage, ChatMessageListItem

router = APIRouter()

# /api/chats/
@router.get("/")
def chat_health():
    return{"status": "ok"}


# api endpoint 
# /api/chats/recent
# curl http://localhost:8080/api/chats/recent/
@router.get("/recent/", response_model = List[ChatMessageListItem])
def chat_list_messages(session: Session = Depends(get_session)):
    query = select(ChatMessage) #sql -> query
    results = session.exec(query).fetchall()[:10]
    return results

#HTTP POST -> payload = {"message": "Hello world"} -> {"message": "Hello world", "id": 1 }
# curl -X POST -d '{"message": "Hello world"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message": "Hello world"}' -H "Content-Type: application/json" https://docker-api-fastapi-python-docker-n7bzb.ondigitalocean.app/api/chats/
@router.post("/", response_model=ChatMessage)
def chat_create_message(
    payload: ChatMessagePayload,
    session: Session = Depends(get_session)
    ):
    data = payload.model_dump() #pydantic function -> turns it into dictonary
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj) #ensures id/primary key added to the obj instance
    # ready to sotre in the database
    return obj