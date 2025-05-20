from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import message

load_dotenv()


app = FastAPI()
app.include_router(message.router)
