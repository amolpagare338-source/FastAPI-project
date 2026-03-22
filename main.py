from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as FastAPIHTTPException
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Print message before request is processed
    print(f"\n=== BEFORE PROCESSING REQUEST ===")
    print(f"HTTP Method: {request.method}")
    print(f"URL Path: {request.url.path}")
    
    # Log using logger as well
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Measure processing time (optional bonus)
    start_time = time.time()
    
    # Process the request
    response = await call_next(request)
    
    # Print message after response is returned
    process_time = time.time() - start_time
    print(f"=== AFTER PROCESSING REQUEST ===")
    print(f"Status Code: {response.status_code}")
    print(f"Processing Time: {process_time:.4f} seconds\n")
    
    return response


# API endpoint
@app.get("/hello")
async def hello():
    return {"message": "Hello, Welcome to FastAPI!"}


# Exception handler for 404 Not Found errors
@app.exception_handler(FastAPIHTTPException)
async def http_exception_handler(request: Request, exc: FastAPIHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "The requested resource was not found"}
        )
    # For other HTTP exceptions, return the original details
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


# Optional: Custom exception handler for general 404 handling
# This catches any unhandled 404 errors
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"message": "The requested resource was not found"}
    )
