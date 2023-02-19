import os
from fastapi import FastAPI
from app.routes import api_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Digital ID")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for route in api_routes: app.include_router(route)  
@app.get("/ping")
def ping(): return 1