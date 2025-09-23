from contextlib import asynccontextmanager

import models
import routers
from database import engine, session
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(routers.router)
app.mount("/static", StaticFiles(directory="static"), "static")
