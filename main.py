from fastapi import FastAPI
from routers.user import router as user_router
from routers.conversation import router as conversation_router
from routers.messages import router as message_router

app = FastAPI()

app.include_router(user_router)
app.include_router(conversation_router)
app.include_router(message_router)
