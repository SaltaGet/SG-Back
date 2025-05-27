from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.middleware import Middleware
from src.config.logging_config import setup_logging
from src.middleware.rate_limit import RateLimitMiddleware
from src.middleware.timing import TimingMiddleware
from fastapi.middleware.cors import CORSMiddleware
import logging
from src.routers.email_router import email_router

setup_logging()

app = FastAPI(title= 'API SaltaGet',
            description='API SaltaGet',
            version='0.0.1',
            docs_url='/',
            )

app.state.rate_limit_ips = {}


app.include_router(router= email_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TimingMiddleware)
app.add_middleware(RateLimitMiddleware)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app.router.lifespan_context = lifespan
