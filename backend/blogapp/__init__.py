from fastapi import FastAPI
from strawberry.asgi import GraphQL

from .core.graphql_api import schema


def create_app():
    graphql_app = GraphQL(schema)
    app = FastAPI()
    app.add_route("/graphql", graphql_app)

    return app
