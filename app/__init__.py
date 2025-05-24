from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

from .logger import logger

from fastapi import HTTPException

def raise_exception(code, detail):
    raise HTTPException(status_code=code, detail=detail)