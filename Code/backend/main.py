from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.analyze import router as analyze_router
from routes.ai_routes import router as ai_router
from routes.version_routes import router as version_router

app = FastAPI()

# Attach routers
app.include_router(analyze_router)
app.include_router(ai_router)
app.include_router(version_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CodeSage Backend Running"}

@app.get("/health")
def health():
    return {"status": "ok"}
