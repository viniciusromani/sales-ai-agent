from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import message
from app.seed import Seed


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await Seed.init()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(message.router)
