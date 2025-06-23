from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from api.db import get_session
from api.ai.agents import get_supervisor
from api.ai.schemas import EmailMessageSchema, SupervisorMessageSchema
from api.ai.services import generate_email_message
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
# curl -X POST -d '{"message": "Give me a very short summary of why it is good to go outside"}' -H "Content-Type: application/json" http://localhost:8080/api/chats/
# curl -X POST -d '{"message": "Say hello."}' -H "Content-Type: application/json" http://localhost:8080/api/chats/

#curl -X POST -d '{"message": "Say hello."}' -H "Content-Type: application/json" https://docker-api-fastapi-python-docker-n7bzb.ondigitalocean.app/api/chats/

#curl -X POST -d '{"message": "Research why it is good to go outside and email me the results."}' -H "Content-Type: application/json" http://localhost:8080/api/chats/


@router.post("/", response_model=SupervisorMessageSchema)
def chat_create_message(
    payload: ChatMessagePayload,
    session: Session = Depends(get_session)
    ):
    data = payload.model_dump() #pydantic function -> turns it into dictonary
    print(data)
    obj = ChatMessage.model_validate(data)
    session.add(obj)
    session.commit()
    supe = get_supervisor()
    msg_data= {
        "messages":[
            {"role": "user",
             "content": f"{payload.message}"
             },
        ]
    }
    result = supe.invoke(msg_data)
    if not result:
        raise HTTPException(stauts_code=400, detail="Error with supervisor")
    messages = result.get("messages")
    if not messages:
        raise HTTPException(stauts_code=400, detail="Error with supervisor")
    return messages[-1]
