from fastapi import FastAPI
from api.chat import router as chat_router
app = FastAPI(
    title="Fix-Mate API",
    description="AI-powered troubleshooting assistant for everyday devices and appliances.",
    version="0.1.0"
)

app.include_router(
    chat_router,
    prefix="/api"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Fix-Mate API",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }