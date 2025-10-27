from fastapi import FastAPI
from .database import engine, Base
from .routers import router

app = FastAPI(title='Battery Monitor Test')
app.include_router(router)

@app.on_event('startup')
async def on_startup():
    # Создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
