from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.seed_service import seed_initial_data

from app.api.auth import router as auth_router
from app.api.resumes import router as resumes_router
from app.api.job_match import router as job_match_router
from app.api.recommendations import router as recommendations_router
from app.api.skill_gap import router as skill_gap_router
from app.api.reports import router as reports_router

# Initialize DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Full-stack production-grade B.Tech AI Resume Analyzer & Job Matcher API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Event
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()

# Global Error Handler (Sanitizes stack traces for security requirement #21)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again or contact support."}
    )

# Include API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(resumes_router, prefix=settings.API_V1_STR)
app.include_router(job_match_router, prefix=settings.API_V1_STR)
app.include_router(recommendations_router, prefix=settings.API_V1_STR)
app.include_router(skill_gap_router, prefix=settings.API_V1_STR)
app.include_router(reports_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "name": settings.PROJECT_NAME,
        "status": "online",
        "docs": "/docs",
        "version": "1.0.0"
    }
