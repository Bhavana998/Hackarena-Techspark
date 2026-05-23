from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response
import time
import logging
from collections import defaultdict
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.requests = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        
        # Clean old requests
        now = time.time()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if now - req_time < self.period
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.calls:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.requests[client_ip].append(now)
        
        # Process request
        response = await call_next(request)
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """Request logging middleware"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log response
        logger.info(f"Response: {response.status_code} - Duration: {duration:.3f}s")
        
        # Add custom header
        response.headers["X-Processing-Time"] = str(duration)
        
        return response

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request"""
    
    async def dispatch(self, request: Request, call_next):
        import uuid
        request_id = str(uuid.uuid4())
        
        # Add to request state
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response

def setup_middleware(app: FastAPI):
    """Setup all middleware"""
    
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)