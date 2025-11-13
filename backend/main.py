import uvicorn
from fastapi import FastAPI
from app.routes import api
from app.db import schema
# from app.db.database import Base
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(api.router)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

schema.Base.metadata.create_all(engine)
# Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)