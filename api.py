from fastapi import FastAPI
from schema.schema import graphql_app
app = FastAPI()

# integration fastapi with strawberry graphql defining a router /graphql
app.include_router(graphql_app, prefix='/graphql')