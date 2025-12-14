from fastapi import FastAPI
from routers.conversation import router as convo_router
from routers.user import router as user_router
from routers.messages import router as message_router

app = FastAPI()

app.include_router(user_router)
app.include_router(convo_router)
app.include_router(message_router)
