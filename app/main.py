from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, users, admin, mock

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Custom Auth System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(mock.router)

@app.get("/")
def read_root():
    return {"message": "Custom Authentication and Authorization System"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}