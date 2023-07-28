import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute, APIRouter
from starlette.requests import Request

from .core import config
from .core.mongodb import mongo_client, get_mongodb_client


async def ping() -> dict:
    return {"Success": "true"}


async def homepage() -> dict:
    return {
        "Mongo url": "123"
    }


async def create_record(request: Request) -> dict:
    mongodb = get_mongodb_client(request)
    await mongodb.records.insert_one({"sample": "record"})
    return {"Success": True}


async def get_records(request: Request) -> list:
    mongodb = get_mongodb_client(request)
    cursor = mongodb.records.find({})
    res = []
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


routes = [
    APIRoute(path="/ping", endpoint=ping, methods=["GET"]),
    APIRoute(path="/", endpoint=homepage, methods=["GET"]),
    APIRoute(path="/create_record", endpoint=create_record, methods=["POST"]),
    APIRoute(path="/get_records", endpoint=get_records, methods=["GET"]),
]

app = FastAPI()
app.include_router(APIRouter(routes=routes))
app.state.mongo_client = mongo_client

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
