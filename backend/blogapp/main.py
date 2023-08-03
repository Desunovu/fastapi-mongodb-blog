import uvicorn
from fastapi import FastAPI

from .core.mongodb import init_odm
from .core.security import routes as security_routes
from .modules import api_test

app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_odm()


app.include_router(api_test.router)
app.include_router(security_routes.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
