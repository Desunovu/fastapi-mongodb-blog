"""Собирает gql схему для strawbery"""

import strawberry

from .queries import Query

schema = strawberry.Schema(query=Query)
