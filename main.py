from fastapi import FastAPI
from core.config import settings
import uvicorn


app = FastAPI(title="Template FastAPI", debug=settings.debug)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=settings.debug)