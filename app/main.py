from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.error import DomainError
from app.routers.auth import AuthRouter
from app.routers.usuarios import UsuariosRouter
from app.routers.vendedores import VendedoresRouter
from app.database import sessionmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()
        
app = FastAPI(lifespan=lifespan)


app.include_router(VendedoresRouter())
app.include_router(UsuariosRouter())
app.include_router(AuthRouter())

@app.exception_handler(DomainError)
async def domain_exception_handler(request, exc: DomainError):
    return JSONResponse(
        content={"detail": exc.message},
        status_code=exc.code
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    
    err = exc.errors()
    
    key = err[0].get("loc")[-1] if len(err) > 0 else "unknown"
    msg = err[0].get("msg") if len(err) > 0 else "Validation error"
    
    return JSONResponse(
        content={key: msg},
        status_code=422
    )

@app.get("/")
async def read_root():
    return {"Hello": "World"}