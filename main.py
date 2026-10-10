import time
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.requests import Request

ALLOWED_ORIGIN = "https://dash-8hjnxi.example.com"
EMAIL = "23f1001027@ds.study.iitm.ac.in"

app = FastAPI()

# CORS first, so the header middleware below wraps it
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
    allow_credentials=False,
)


@app.middleware("http")
async def add_request_headers(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"
    return response


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/stats")
def stats(values: str = Query("")):
    try:
        nums = [int(v) for v in values.split(",") if v.strip()]
    except ValueError:
        return JSONResponse({"error": "values must be comma-separated integers"}, status_code=400)
    if not nums:
        return JSONResponse({"error": "no values provided"}, status_code=400)
    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": round(sum(nums) / len(nums), 6),
    }
