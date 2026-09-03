import asyncio
import io
import os

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from rembg import new_session, remove
from starlette.responses import Response

MAX_BYTES = 10 * 1024 * 1024
MAX_PIXELS = 12_000_000
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
queue = asyncio.Semaphore(1)
session = None

app = FastAPI(title="Tiny Product Lab Photo API", docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://photo.tinylabpro.com",
        "https://tinyproductlab.github.io",
        "http://127.0.0.1:4174",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["content-type"],
)


@app.get("/healthz")
def healthz():
    return {"ok": True}


def remove_in_memory(data: bytes) -> bytes:
    global session
    if session is None:
        session = new_session("isnet-general-use")
    return remove(data, session=session, force_return_bytes=True)


@app.post("/v1/remove-background")
async def remove_background(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(415, "Only JPG, PNG and WebP images are supported.")
    data = await file.read(MAX_BYTES + 1)
    await file.close()
    if not data or len(data) > MAX_BYTES:
        raise HTTPException(413, "Image must be no larger than 10 MB.")
    try:
        with Image.open(io.BytesIO(data)) as image:
            width, height = image.size
            if width * height > MAX_PIXELS:
                raise HTTPException(413, "Image must be no larger than 12 megapixels.")
            image.verify()
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError):
        raise HTTPException(400, "The uploaded file is not a valid image.")

    try:
        async with queue:
            result = await asyncio.wait_for(run_in_threadpool(remove_in_memory, data), timeout=180)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Processing timed out. Please try a smaller image.")
    except Exception:
        raise HTTPException(500, "Background removal did not complete. Please try again.")
    return Response(result, media_type="image/png", headers={"Cache-Control": "no-store"})
