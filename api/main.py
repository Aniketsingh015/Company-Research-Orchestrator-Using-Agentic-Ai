"""FastAPI application for Company Research Agent."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from api.routes import companies, research, health
from config.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Company Research Agent API",
    description="Multi-agent AI system for comprehensive company research",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# -----------------------------------------------------
# CORS
# -----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------
# Request timing middleware
# -----------------------------------------------------

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)

    return response


# -----------------------------------------------------
# Routers
# -----------------------------------------------------

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])
app.include_router(research.router, prefix="/api/v1", tags=["Research"])


# -----------------------------------------------------
# Root Endpoint
# -----------------------------------------------------

@app.get("/")
async def root():

    return {
        "name": "Company Research Agent API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/api/v1/health",
        "companies": "/api/v1/companies/{company_name}",
        "research": "/api/v1/research/{company_name}"
    }


# -----------------------------------------------------
# Startup
# -----------------------------------------------------

@app.on_event("startup")
async def startup_event():

    logger.info("🚀 Company Research Agent API starting up...")
    logger.info(f"📊 Supabase URL: {settings.supabase_url}")
    logger.info(f"🤖 LLM Provider: {settings.llm_provider}")
    logger.info(f"🤖 Model: {settings.default_model}")


# -----------------------------------------------------
# Shutdown
# -----------------------------------------------------

@app.on_event("shutdown")
async def shutdown_event():

    logger.info("🛑 Company Research Agent API shutting down...")