# FastAPI
from fastapi import FastAPI

# Routers
from routers.user import router as user_router
from routers.conversation import router as conversation_router
from routers.messages import router as message_router

app = FastAPI(
    title="Chatbot Wrapper Backend",
    description="""
Built by **Aarush Srivatsa**  
GitHub: https://github.com/AarushSrivatsa  
Linkedin: https://www.linkedin.com/in/aarushsrivatsa/
""")

app.include_router(user_router)
app.include_router(conversation_router)
app.include_router(message_router)
