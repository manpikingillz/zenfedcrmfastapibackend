from fastapi import FastAPI
from .database import Base, engine
from app.routes.router import router as api_router

# Create the FastAPI app instance
app = FastAPI()

# Create the database tables (if they don't exist)
Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api/v1", tags=["ZenFed CRM v1 Endpoints"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
