"""
Main FastAPI application for Fraud Detection Dashboard Backend
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from datetime import datetime

from backend.config import settings
from backend.api.v1.router import api_router
from backend.data.data_loader import data_loader
from backend.models.schemas import HealthCheckResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Load data
    logger.info("Starting Fraud Detection Dashboard API...")
    logger.info(f"Data file: {settings.DATA_FILE_PATH}")
    
    try:
        # Preload data in background (optional, data loads on first request)
        # data_loader.load_data()
        logger.info("API ready to accept requests")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    # 🚨 Fraud Detection Dashboard API
    
    **Production-ready backend for real-time fraud detection and monitoring.**
    
    ## 📊 Dashboard Tiles Coverage
    
    ### Tier 1: Executive Overview
    - Real-time fraud pulse KPIs
    - High-risk transaction feed
    - Smart alert system
    
    ### Tier 2: Operational Command Center
    - Fraud velocity heatmap
    - Fraud type breakdown
    - Behavioral anomaly detection
    
    ### Tier 3: Investigation Workbench
    - Network graph analysis
    - Transaction explanations
    - Money mule detection
    
    ### Tier 4: Model Performance
    - Model health monitoring
    - Confusion matrix
    - Feature importance
    
    ### Tier 5: Business Intelligence
    - Financial impact analysis
    - Customer experience metrics
    - Temporal trends & forecasting
    - Merchant/channel risk matrix
    
    ## 🎯 Key Features
    - **Real-time Processing**: Sub-second response times
    - **Network Analysis**: Graph-based fraud ring detection
    - **Predictive Analytics**: ML-powered risk scoring
    - **Explainable AI**: Feature importance for every prediction
    - **Business Metrics**: ROI, cost impact, customer experience
    
    ## 🔧 Tech Stack
    - FastAPI (async Python framework)
    - Pandas (data processing)
    - Pydantic (data validation)
    - Graph algorithms (network analysis)
    
    ## 👨‍💻 Author
    **Masood Nazari**  
    Business Intelligence Analyst | Data Science | AI | Clinical Research
    
    📧 M.Nazari@soton.ac.uk  
    🌐 https://michaeltheanalyst.github.io/  
    💼 linkedin.com/in/masood-nazari  
    🔗 github.com/michaeltheanalyst
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
# Allow all origins in production (public API), restrict in development
if settings.DEBUG:
    # Development: Use specific origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    # Production: Allow all origins (public API)
    # Use regex to allow all Vercel domains (preview + production)
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https://.*\.vercel\.app",  # All Vercel deployments
        allow_credentials=False,  # Must be False when using regex
        allow_methods=["*"],
        allow_headers=["*"],
    )


# Middleware for request logging and timing
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log request details
    logger.info(
        f"{request.method} {request.url.path} "
        f"completed in {duration:.3f}s with status {response.status_code}"
    )
    
    # Add timing header
    response.headers["X-Process-Time"] = str(duration)
    
    return response


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """
    **System Health Check** - Verify API is running and data is loaded
    
    Returns:
    - API status
    - Data loading status
    - Dataset information
    """
    data_info = data_loader.data_info
    
    return HealthCheckResponse(
        status="healthy" if data_info.get("loaded", False) else "degraded",
        timestamp=datetime.now(),
        data_loaded=data_info.get("loaded", False),
        data_info=data_info if data_info.get("loaded", False) else None
    )


@app.get("/", tags=["System"])
async def root():
    """
    **Root Endpoint** - API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "api_v1": settings.API_V1_PREFIX
    }


# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Run with: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )

